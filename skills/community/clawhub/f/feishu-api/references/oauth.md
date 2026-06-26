# OAuth 用户授权流程

## 概述

OAuth 2.0 用于获取代表用户的 `user_access_token`，实现"用户委托"能力。

## 授权流程

```
用户 → 授权页面 → 用户同意 → 回调获取 code → 换取 user_access_token
```

### Step 1: 构建授权 URL

```
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={app_id}&redirect_uri={encoded_redirect_uri}&state={random_state}
```

参数说明：
- `app_id`: 应用 ID（cli_xxx）
- `redirect_uri`: 授权后跳转的回调地址（需在应用配置中注册）
- `state`: 随机字符串，用于防止 CSRF

### Step 2: 用户授权

用户访问授权 URL，在飞书页面确认授权。

### Step 3: 获取 code

授权成功后会回调到 `redirect_uri`，URL 参数中携带 `code`：

```
https://your-server.com/callback?code=xxx&state=xxx
```

### Step 4: 换取 user_access_token

```python
import ssl, urllib.request, json

def exchange_code_for_token(app_id, app_secret, code):
    url = 'https://open.feishu.cn/open-apis/authen/v1/oidc/access_token'
    data = json.dumps({
        'grant_type': 'authorization_code',
        'code': code,
        'app_id': app_id,
        'app_secret': app_secret
    }).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        resp = json.loads(r.read())
    return resp.get('data', {}).get('access_token')
```

返回数据结构：
```json
{
  "code": 0,
  "data": {
    "access_token": "u-xxx",
    "token_type": "Bearer",
    "expires_in": 7200,
    "refresh_token": "r-xxx",
    "scope": "contact:user.id:readonly",
    "open_id": "ou_xxx",
    "union_id": "on_xxx"
  }
}
```

### Step 5: 刷新 token

`user_access_token` 有效期短，过期前用 refresh_token 刷新：

```python
def refresh_user_token(app_id, app_secret, refresh_token):
    url = 'https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token'
    data = json.dumps({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'app_id': app_id,
        'app_secret': app_secret
    }).encode()
    # ... 同上调用
```

## 安全建议

1. **state 参数**：生成随机字符串，验证回调时比对，防止 CSRF
2. **code 一次性**：code 只能使用一次，用完即失效
3. **HTTPS**：生产环境必须使用 HTTPS
4. **Token 存储**：加密存储 refresh_token，不要明文保存
5. **最小范围**：申请最小必要的权限范围

## 权限范围

常用 scope：

| Scope | 说明 |
|-------|------|
| `docx:document:readonly` | 只读文档 |
| `docx:document` | 读写文档 |
| `bitable:app` | 多维表格 |
| `drive:drive` | 云文档 |
| `contact:user.id:readonly` | 获取用户 ID |

在飞书应用管理后台配置应用的「权限管理」，添加所需权限。