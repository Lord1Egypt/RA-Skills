import json, urllib.request, urllib.error

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json'))
token = 't-g1043jexJNXU6IOGYC26VWSWESLRGIMMOWRXJWYS'
doc_token = 'KH6qdDlNuoACh4xSaPTcFFr3npc'

tests = [
    (3, 'heading1'),
    (4, 'heading2'),
    (5, 'heading3'),
    (6, 'bullet'),
    (7, 'ordered'),
]

for bt, key in tests:
    blocks = [{'block_type': bt, key: {'elements': [{'type': 'text_run', 'text_run': {'content': 'Test content'}}], 'style': {}}}]
    url = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks/' + doc_token + '/children'
    data = json.dumps({'children': blocks}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token})
    try:
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read())
        code = result.get('code')
        print('block_type', bt, '(' + key + '): OK code=' + str(code))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print('block_type', bt, '(' + key + '): Error ' + str(e.code) + ' - ' + body[:100])
