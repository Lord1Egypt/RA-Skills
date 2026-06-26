---
name: feishu-api
description: |
  飞书开放平台 API 技能。用于：(1) 调用飞书开放 API 完成插件以外的操作（如批量写入、权限管理、文件夹操作等）；(2) 实现 OAuth 用户授权流程；(3) 批量数据处理。
  
  当用户提到飞书 API、飞书开放平台、OAuth 授权、user_access_token，或需要批量操作飞书数据（多维表格批量写入/删除、权限配置、云文档管理）时触发。
---

# 飞书开放平台 API

本技能提供直接调用飞书开放 API 的能力，作为飞书插件工具的补充。

## 核心概念

### 认证方式

| 类型 | 用途 | 有效期 |
|------|------|--------|
| `tenant_access_token` | 应用身份调用 API | 2小时 |
| `user_access_token` | 代表用户操作 | 有效期短，需刷新 |

**重要**：所有脚本中不得硬编码 `app_id`、`app_secret`、`access_token`。从配置文件读取或使用环境变量。

### 读取凭据

飞书凭据存储在 `~/.openclaw/openclaw.json` 的 `channels.feishu` 下：

```python
import json
with open('/root/.openclaw/openclaw.json') as f:
    config = json.load(f)
feishu_cfg = config.get('channels', {}).get('feishu', {})
APP_ID = feishu_cfg.get('appId', '')
APP_SECRET = feishu_cfg.get('appSecret', '')
```

## 典型工作流

### 1. 获取 Token

```python
import ssl, urllib.request, json

def get_app_access_token(app_id, app_secret):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        return json.loads(r.read()).get('tenant_access_token')
```

### 2. 调用 API

```python
def call_feishu_api(url, method, token, payload=None):
    ctx = ssl._create_unverified_context()
    data = json.dumps(payload, ensure_ascii=False).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return json.loads(r.read())
```

### 3. 批量操作多维表格

```python
# 批量创建记录
url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'
payload = {'records': [{'fields': {'字段名': '值'}} for item in items]}
result = call_feishu_api(url, 'POST', token, payload)

# 批量删除记录
url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete'
payload = {'records': ['record_id_1', 'record_id_2']}
result = call_feishu_api(url, 'POST', token, payload)
```

### 4. 权限管理

```python
# 添加协作者
url = f'https://open.feishu.cn/open-apis/drive/v1/permissions/{file_token}/members?type=bitable'
payload = {
    'member_type': 'openid',      # 或 email, userid, unionid
    'member_id': 'ou_xxx',        # 用户 open_id
    'perm': 'edit'                 # view | edit | full_access
}
result = call_feishu_api(url, 'POST', token, payload)
```

## 常用 API 端点

| 功能 | 端点 |
|------|------|
| 批量创建多维表格记录 | `POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create` |
| 批量删除多维表格记录 | `POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete` |
| 更新记录 | `PUT /bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}` |
| 添加权限成员 | `POST /drive/v1/permissions/{file_token}/members?type={type}` |
| 列出权限成员 | `GET /drive/v1/permissions/{file_token}/members?type={type}` |
| 创建文件夹 | `POST /drive/v1/files/create_folder` |
| 移动文件 | `POST /drive/v1/files/{file_token}/move` |
| 上传文件 | `POST /drive/v1/files/upload_all` |

## 详细参考

- **OAuth 授权流程**：参见 [references/oauth.md](references/oauth.md)
- **多维表格 API**：参见 [references/bitable.md](references/bitable.md)
- **云文档管理**：参见 [references/drive.md](references/drive.md)

## 数据安全准则

1. **不硬编码凭据** - 始终从配置文件读取
2. **不输出敏感信息** - 不打印 token、secret 等
3. **最小权限** - 仅申请所需的权限范围
4. **定期刷新** - token 过期前刷新

## 速率限制

- 普通 API：每应用每秒 10 请求
- 上传文件：每应用每分钟 60 次
- 批量接口：每批最大 50 条记录