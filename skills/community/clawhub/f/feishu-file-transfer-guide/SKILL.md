# OpenClaw 飞书文件传输技术分享

> **作者**: SwingMonkey
>
> **日期**: 2026-03-14  
>
> **适用**: OpenClaw Agent 飞书文件传输场景

---

## 一、问题背景

OpenClaw 的 `message` 工具在飞书渠道发送本地文件时，会直接发送文件路径而非上传文件内容。需要通过飞书 API 实现真正的文件上传和发送。

---

## 二、核心流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  获取 Token  │ ──▶ │  上传文件   │ ──▶ │  发送消息   │
│  (Step 1)   │     │  (Step 2)   │     │  (Step 3)   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   tenant_            file_key            消息送达
   access_token       (文件标识)          飞书用户
```

---

## 三、详细步骤

### Step 1: 获取 tenant_access_token

**接口**: `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`

**请求头**:

```
Content-Type: application/json
```

**请求体**:

```json
{
  "app_id": "cli_xxxxxxxxxx",
  "app_secret": "xxxxxxxxxx"
}
```

**PowerShell 实现**:

```powershell
$tokenResponse = Invoke-RestMethod `
    -Uri 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' `
    -Method POST `
    -Headers @{'Content-Type'='application/json'} `
    -Body '{"app_id":"cli_xxxxxxxxxx","app_secret":"xxxxxxxxxx"}'

$TOKEN = $tokenResponse.tenant_access_token
```

**返回示例**:

```json
{
  "code": 0,
  "msg": "ok",
  "tenant_access_token": "t-xxxxxxxxxx",
  "expire": 7200
}
```

---

### Step 2: 上传文件获取 file_key

**接口**: `POST https://open.feishu.cn/open-apis/im/v1/files`

**关键要点**:

- 使用 **multipart/form-data** 格式
- **文件名使用英文**（避免中文编码问题）
- 必须包含 `file` 和 `file_type` 字段

**Python 实现**（推荐）:

```python
import urllib.request
import json
import ssl

# SSL 配置
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def upload_file(token, file_path, display_name):
    """
    上传文件到飞书
    
    Args:
        token: tenant_access_token
        file_path: 本地文件路径
        display_name: 显示文件名（建议英文）
    
    Returns:
        file_key: 文件标识
    """
    url = 'https://open.feishu.cn/open-apis/im/v1/files'
    
    # 读取文件
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # 构建 multipart
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = b''
    
    # file 字段
    body += f'------{boundary}\r\n'.encode('utf-8')
    body += f'Content-Disposition: form-data; name="file"; filename="{display_name}"\r\n'.encode('utf-8')
    body += b'Content-Type: application/octet-stream\r\n\r\n'
    body += file_data
    body += b'\r\n'
    
    # file_type 字段
    body += f'------{boundary}\r\n'.encode('utf-8')
    body += b'Content-Disposition: form-data; name="file_type"\r\n\r\n'
    body += b'stream\r\n'
    
    # 结束
    body += f'------{boundary}--\r\n'.encode('utf-8')
    
    # 请求
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', f'multipart/form-data; boundary=----{boundary}')
    
    with urllib.request.urlopen(req, context=ssl_context) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['data']['file_key']

# 使用示例（支持中文文件名）
FILE_KEY = upload_file(
    token='t-xxxxxxxxxx',
    file_path='/path/to/your/file.docx',
    display_name='语文.docx'  # 支持中文文件名
)
```

**返回示例**:

```json
{
  "code": 0,
  "data": {
    "file_key": "file_v3_00vp_xxxxxxxxxx"
  },
  "msg": "success"
}
```

---

### Step 3: 发送文件消息

**接口**: `POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id`

**请求头**:

```
Authorization: Bearer {tenant_access_token}
Content-Type: application/json; charset=utf-8
```

**请求体**:

```json
{
  "receive_id": "ou_xxxxxxxxxx",
  "msg_type": "file",
  "content": "{\"file_key\":\"file_v3_00vp_xxxxxxxxxx\"}"
}
```

**PowerShell 实现**:

```powershell
$body = @{
    receive_id = "ou_xxxxxxxxxx"
    msg_type = "file"
    content = '{"file_key":"file_v3_00vp_xxxxxxxxxx"}'
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' `
    -Method POST `
    -Headers @{
        'Authorization' = "Bearer $TOKEN"
        'Content-Type' = 'application/json; charset=utf-8'
    } `
    -Body $body
```

**返回示例**:

```json
{
  "code": 0,
  "data": {
    "message_id": "om_xxxxxxxxxx",
    "msg_type": "file"
  },
  "msg": "success"
}
```

---

## 四、完整示例代码

### Python 完整版

```python
#!/usr/bin/env python3
"""
OpenClaw 飞书文件传输工具
用法: python feishu_transfer.py <file_path> <receive_id>
"""

import urllib.request
import json
import ssl
import os
import sys

class FeishuFileTransfer:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    def get_token(self):
        """获取 tenant_access_token"""
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        data = {'app_id': self.app_id, 'app_secret': self.app_secret}
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as res:
            result = json.loads(res.read().decode('utf-8'))
            return result['tenant_access_token']
    
    def upload_file(self, token, file_path, display_name=None):
        """上传文件"""
        if display_name is None:
            display_name = os.path.basename(file_path)
        
        url = 'https://open.feishu.cn/open-apis/im/v1/files'
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # 构建 multipart
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = b''
        body += f'------{boundary}\r\n'.encode('utf-8')
        body += f'Content-Disposition: form-data; name="file"; filename="{display_name}"\r\n'.encode('utf-8')
        body += b'Content-Type: application/octet-stream\r\n\r\n'
        body += file_data
        body += b'\r\n'
        body += f'------{boundary}\r\n'.encode('utf-8')
        body += b'Content-Disposition: form-data; name="file_type"\r\n\r\n'
        body += b'stream\r\n'
        body += f'------{boundary}--\r\n'.encode('utf-8')
        
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', f'multipart/form-data; boundary=----{boundary}')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as res:
            result = json.loads(res.read().decode('utf-8'))
            return result['data']['file_key']
    
    def send_file(self, token, file_key, receive_id):
        """发送文件消息"""
        url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id'
        data = {
            'receive_id': receive_id,
            'msg_type': 'file',
            'content': json.dumps({'file_key': file_key})
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            method='POST'
        )
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as res:
            return json.loads(res.read().decode('utf-8'))

# 使用示例
if __name__ == '__main__':
    # 配置（替换为你的凭证）
    APP_ID = 'cli_xxxxxxxxxx'
    APP_SECRET = 'xxxxxxxxxx'
    FILE_PATH = '/path/to/your/file.docx'
    RECEIVE_ID = 'ou_xxxxxxxxxx'
    
    # 执行传输（支持中文文件名）
    transfer = FeishuFileTransfer(APP_ID, APP_SECRET)
    token = transfer.get_token()
    file_key = transfer.upload_file(token, FILE_PATH, '语文.docx')  # 中文文件名
    result = transfer.send_file(token, file_key, RECEIVE_ID)
    
    print(f'发送成功: {result}')
```

---

## 五、关键注意事项

### 1. 文件名编码问题

- **问题**: 早期中文文件名可能显示为乱码
- **解决**: 确保 multipart 请求中 `file_name` 字段正确编码为 UTF-8
- **验证**: 中文文件名 `语文.docx` 可以正常显示

### 2. 文件大小限制

- **问题**: 不能上传空文件（大小为 0 字节）
- **解决**: 确保文件有实际内容

### 3. 编码设置

- **PowerShell**: 使用 `-ContentType 'application/json; charset=utf-8'`
- **Python**: 使用 `encode('utf-8')` 处理中文

### 4. 避免重复发送

- 确认上传成功后再执行发送步骤
- 不要多次调用发送 API

---

## 六、常见问题排查

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| 文件名显示为乱码 | 编码问题 | 确保 `file_name` 字段 UTF-8 编码 |
| 上传返回 400 | 文件为空 | 确保文件有内容 |
| 发送后文件名是 UUID | 未正确设置文件名 | 在上传时指定 `filename` |
| 中文内容乱码 | 编码问题 | 使用 `charset=utf-8` |

---

## 七、参考文档

- [飞书开放平台 - 上传文件](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [飞书开放平台 - 发送消息](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)

---

*本文档由 SwingMonkey 整理分享，供社区参考使用*
