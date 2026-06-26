import json, urllib.request, urllib.error, datetime

config = json.load(open('filepath'))
url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
data = json.dumps({'app_id': config['app_id'], 'app_secret': config['app_secret']}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    token = json.loads(r.read())['tenant_access_token']

chat_id = 'oc_3b77de8ba3bc9aa5512abfd8881604bb'
url2 = 'https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=' + chat_id + '&page_size=50'
req2 = urllib.request.Request(url2, headers={'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req2) as r:
    result = json.loads(r.read())

items = result.get('data', {}).get('items', [])
print('Total messages:', len(items))
print()

msgs = []
for it in items:
    msg_type = it.get('msg_type')
    sender = it.get('sender', {}).get('id', '')
    ct = int(it.get('create_time', 0)) // 1000
    dt = datetime.datetime.fromtimestamp(ct).strftime('%Y-%m-%d %H:%M:%S') if ct else 'N/A'
    body = json.loads(it.get('body', {}).get('content', '{}'))

    if msg_type == 'text':
        content = body.get('text', '')
        msgs.append({'time': dt, 'type': 'text', 'sender': sender, 'content': content})
        print(f"[text] {dt} | {sender} | {content}")
    elif msg_type == 'post':
        # rich text post
        title = body.get('title', '')
        parts = []
        for section in body.get('content', []):
            for item in section:
                tag = item.get('tag', '')
                if tag == 'text':
                    parts.append(item.get('text', ''))
                elif tag == 'at':
                    parts.append('@' + item.get('user_id', ''))
        content = title + ' ' + ''.join(parts)
        msgs.append({'time': dt, 'type': 'post', 'sender': sender, 'content': content})
        print(f"[post] {dt} | {sender} | {title} | {''.join(parts)}")
    elif msg_type == 'system':
        template = body.get('template', '')
        from_user = ','.join(body.get('from_user', []))
        to_chatters = ','.join(body.get('to_chatters', []))
        content = template.format(from_user=from_user, to_chatters=to_chatters)
        msgs.append({'time': dt, 'type': 'system', 'sender': 'system', 'content': content})
        print(f"[system] {dt} | {content}")

# create document
url3 = 'https://open.feishu.cn/open-apis/docx/v1/documents'
data3 = json.dumps({'title': 'test群聊消息记录'}).encode('utf-8')
req3 = urllib.request.Request(url3, data=data3, method='POST', headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req3) as r:
    doc_result = json.loads(r.read())

print()
print('doc create code:', doc_result.get('code'))
if doc_result.get('code') != 0:
    print('failed:', doc_result.get('msg'))
    import sys
    sys.exit(1)

doc_token = doc_result['data']['document']['document_id']
print('doc_token:', doc_token)

# get root block
url4 = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks?page_size=50'
req4 = urllib.request.Request(url4, headers={'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req4) as r:
    blocks_result = json.loads(r.read())
root_id = blocks_result['data']['items'][0]['block_id']

def h2(content):
    return {'block_type': 4, 'heading2': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def bullet(content):
    return {'block_type': 12, 'bullet': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def text(content):
    return {'block_type': 2, 'text': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

doc_blocks = [h2('群聊消息记录')]
for m in msgs:
    type_icon = {'text': '', 'post': '', 'system': '[系统] '}.get(m['type'], '')
    line = '%(time)s | %(type_icon)s%(content)s' % {'time': m['time'], 'type_icon': type_icon, 'content': m['content']}
    doc_blocks.append(bullet(line))

url5 = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks/' + root_id + '/children'
data5 = json.dumps({'children': doc_blocks}).encode('utf-8')
req5 = urllib.request.Request(url5, data=data5, method='POST', headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req5) as r:
    write_result = json.loads(r.read())

print('write code:', write_result.get('code'))
if write_result.get('code') == 0:
    print('doc_url:', 'https://feishu.cn/docx/' + doc_token)
else:
    print('write failed:', write_result.get('msg'))
