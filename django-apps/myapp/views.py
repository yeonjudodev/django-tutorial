from django.shortcuts import render, HttpResponse, redirect 
from django.views.decorators.csrf import csrf_exempt

countid = 3
titledict = [
    {'id':1, 'title':'routing', 'body':'What routing is ...'},
    {'id':2, 'title':'view', 'body':'What view is ...'},
    {'id':3, 'title':'model', 'body':'What model is ...'}
]

def HTMLtemplate(article, id=None):
    global titledict
    contextUI = ''
    if id != None:
        contextUI = f'''
                <li>
                    <form action="/delete/" method="post">
                        <input type="hidden" name="id" value={id}>
                        <input type="submit" value="delete">
                    </form>
                    
                </li>
                <li><a href="/update/{id}">update</a></li>
            '''

    titles = ''
    for info in titledict:
        titles += f'<li><a href="/read/{info["id"]}">{info["title"]}</a></li>'
    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {titles}
            </ol>
            {article}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
    <h2>Welcome to Django tutorials.</h2> Hello, Django!
    '''
    return HttpResponse(HTMLtemplate(article))

@csrf_exempt
def create(request):
    global countid

    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="제목"></p>
                <p><textarea name="body" placeholder="내용"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLtemplate(article))
    elif request.method == 'POST':
        countid = countid + 1
        title = request.POST['title']
        body = request.POST['body']
        newtitledict = {"id":countid, "title":title, "body":body}
        titledict.append(newtitledict)
        return redirect(f'/read/{countid}')

def read(request, id):
    global titledict
    article = ''
    for info in titledict:
        if info['id'] == int(id):
            article = f'<h2>{info["title"]}</h2>{info["body"]}'
    return HttpResponse(HTMLtemplate(article, id))

@csrf_exempt
def delete(request):
    global titledict
    if request.method == 'POST':
        id = request.POST['id']
        newtitledict = []
        for info in titledict:
            if info['id'] != int(id):
                newtitledict.append(info)
    titledict = newtitledict
    return redirect('/')


@csrf_exempt
def update(request, id):
    global titledict
    if request.method == 'GET':
        for info in titledict:
            if info['id'] == int(id):
                 selectedtitle = {
                   "title":info['title'],
                    "body":info['body']
                    }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="제목" value={selectedtitle["title"]}></p>
                <p><textarea name="body" placeholder="내용">{selectedtitle["body"]}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLtemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for info in titledict:
            if info['id'] == int(id):
                info['title'] = title
                info['body'] = body
        return redirect(f'/read/{id}')