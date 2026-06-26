import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import json, os

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json', encoding='utf-8'))

client = lark.Client.builder() \
    .app_id(config['app_id']) \
    .app_secret(config['app_secret']) \
    .log_level(lark.LogLevel.ERROR) \
    .build()

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
target_size = 15914
matching = [(f, os.path.getsize(os.path.join(desktop, f))) for f in os.listdir(desktop) 
            if f.endswith('.xlsx') and os.path.getsize(os.path.join(desktop, f)) == target_size]
filename, _ = matching[0]
filepath = os.path.join(desktop, filename)
print('File:', filepath)

# Upload file using SDK
with open(filepath, 'rb') as f:
    file_data = f.read()

request = CreateFileRequest.builder() \
    .request_body(CreateFileRequestBody.builder()
        .file_type("xlsx")
        .file_name(filename)
        .file(file_data)
        .build()) \
    .build()

response = client.im.v1.file.create(request)
print('code:', response.code, 'msg:', response.msg)
if response.success():
    print('file_key:', response.data.file_key)
else:
    print('raw:', response.raw.content[:200] if hasattr(response, 'raw') else 'no raw')
