import json, urllib.request, urllib.error

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json'))
token = 't-g1043jexJNXU6IOGYC26VWSWESLRGIMMOWRXJWYS'
doc_token = 'KH6qdDlNuoACh4xSaPTcFFr3npc'

url = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks/' + doc_token + '/children'

tests = [
    ({'block_type': 6, 'bullet': {'elements': [{'type': 'text', 'text': {'content': 'Bullet item'}}], 'style': {}}}, 'bullet with text type'),
    ({'block_type': 9, 'code': {'elements': [{'type': 'text_run', 'text_run': {'content': 'Code line'}}], 'style': {'language': 1}}}, 'code block'),
    ({'block_type': 10, 'quote': {'elements': [{'type': 'text_run', 'text_run': {'content': 'Quote text'}}], 'style': {}}}, 'quote block'),
    ({'block_type': 2, 'paragraph': {'elements': [{'type': 'text_run', 'text_run': {'content': 'Para text'}}], 'style': {}}}, 'paragraph'),
]

for block, desc in tests:
    data = json.dumps({'children': [block]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token})
    try:
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read())
        print(desc + ': OK code=' + str(result.get('code')))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(desc + ': Error ' + str(e.code) + ' - ' + body[:120])
