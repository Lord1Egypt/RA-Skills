# 云文档（Drive）API

## 权限管理

### 添加协作者

```
POST /drive/v1/permissions/{file_token}/members?type={type}
```

参数：
- `file_token`: 文件/多维表格的 token
- `type`: bitable | doc | sheet | folder

请求体：

```python
payload = {
    'member_type': 'openid',      # openid | email | userid | unionid | openchat | opendepartmentid
    'member_id': 'ou_xxx',       # 用户 ID
    'perm': 'edit',              # view | edit | full_access
    'type': 'bitable'            # 与 URL 参数一致
}
```

响应：

```python
{'code': 0, 'msg': 'Success'}
```

常见错误码：
- `230013`: 无权限（应用没有被授予管理此文档的权限）
- `99991663`: 成员已在协作者列表中

### 移除协作者

```
DELETE /drive/v1/permissions/{file_token}/members?type={type}&member_id={member_id}&member_type={member_type}
```

### 列出协作者

```
GET /drive/v1/permissions/{file_token}/members?type={type}
```

## 文件管理

### 创建文件夹

```
POST /drive/v1/files/create_folder
```

```python
payload = {
    'name': '文件夹名',
    'folder_token': 'fldcnxxx'  # 父文件夹 token，根目录则留空
}
```

### 移动文件

```
POST /drive/v1/files/{file_token}/move
```

```python
payload = {
    'type': 'bitable',  # bitable | doc | sheet | folder
    'folder_token': 'fldcnxxx'  # 目标文件夹
}
```

### 复制文件

```
POST /drive/v1/files/{file_token}/copy
```

```python
payload = {
    'type': 'bitable',
    'folder_token': 'fldcnxxx',
    'name': '新文件名'  # 可选
}
```

### 上传文件

```
POST /drive/v1/files/upload_all
```

```python
import mimetypes, os, urllib.request, json

file_path = '/path/to/file.pdf'
file_name = os.path.basename(file_path)
mime = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

with open(file_path, 'rb') as f:
    file_data = f.read()

url = 'https://open.feishu.cn/open-apis/drive/v1/files/upload_all'
boundary = '----FormBoundary7MA4YWxkTrZu0gW'
body = f'''--{boundary}
Content-Disposition: form-data; name="file"; filename="{file_name}"
Content-Type: {mime}

{file_data.decode('latin-1')}
--{boundary}
Content-Disposition: form-data; name="parent_type"

drive
--{boundary}
Content-Disposition: form-data; name="parent_node"

{fldcnxxx}
--{boundary}
Content-Disposition: form-data; name="size"

{len(file_data)}
--{boundary}
Content-Disposition: form-data; name="file_name"

{file_name}
--{boundary}--
'''

req = urllib.request.Request(url, data=body.encode('utf-8'), method='POST')
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

ctx = ssl._create_unverified_context()
with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
    resp = json.loads(r.read())
# resp['data']['file_token'] 即上传文件的 token
```

## 文档类型

| type | 说明 |
|------|------|
| `docx` | 文档 |
| `sheet` | 电子表格 |
| `bitable` | 多维表格 |
| `folder` | 文件夹 |
| `mindnote` | 思维导图 |
| `file` | 文件 |

从 URL 获取：
- 文档: `https://xxx.feishu.cn/docx/ABC123` → token: `ABC123`
- 多维表格: `https://xxx.feishu.cn/base/ABC123?table=XYZ` → app_token: `ABC123`, table_id: `XYZ`