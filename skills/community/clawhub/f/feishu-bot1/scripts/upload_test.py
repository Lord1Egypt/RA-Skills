import json, os, requests, urllib.parse

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json', encoding='utf-8'))
r = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', 
                  json={'app_id': config['app_id'], 'app_secret': config['app_secret']})
token = r.json()['tenant_access_token']

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
target_size = 15914
matching = [(f, os.path.getsize(os.path.join(desktop, f))) for f in os.listdir(desktop) 
            if f.endswith('.xlsx') and os.path.getsize(os.path.join(desktop, f)) == target_size]
filename, _ = matching[0]
filepath = os.path.join(desktop, filename)
encoded_name = urllib.parse.quote(filename)

# Use data= instead of files= for file upload (plain binary)
url = f'https://open.feishu.cn/open-apis/im/v1/files?file_name={encoded_name}&file_type=xlsx'
with open(filepath, 'rb') as f:
    file_data = f.read()

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/octet-stream'
}
r2 = requests.post(url, data=file_data, headers=headers)
print('data=bytes:', r2.status_code, r2.json().get('code'), r2.json().get('msg', '')[:80])

# Try multipart with correct format
url3 = f'https://open.feishu.cn/open-apis/im/v1/files?file_name={encoded_name}&file_type=xlsx'
with open(filepath, 'rb') as f:
    files = {'file': (filename, f)}
    r3 = requests.post(url3, files=files, headers={'Authorization': 'Bearer ' + token})
print('multipart:', r3.status_code, r3.json().get('code'), r3.json().get('msg', '')[:80])

# Try with explicit filename in multipart
url4 = f'https://open.feishu.cn/open-apis/im/v1/files?file_name={encoded_name}&file_type=xlsx'
with open(filepath, 'rb') as f:
    files = {'file': (filename, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    r4 = requests.post(url4, files=files, headers={'Authorization': 'Bearer ' + token})
print('multipart+ct:', r4.status_code, r4.json().get('code'), r4.json().get('msg', '')[:80])
