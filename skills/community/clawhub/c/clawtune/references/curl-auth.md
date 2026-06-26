# ClawTune curl templates: auth

默认基址：

```bash
export CLAWTUNE_BASE_URL="https://clawtune.aqifun.com/api/v1"
```

## 1. Bootstrap

```bash
curl -X POST "$CLAWTUNE_BASE_URL/bootstrap" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "openclaw",
    "user_ref": "demo-user-001"
  }'
```

响应中重点关注：
- `installation_id`
- `access_token`
- `expires_in`
- `refresh_token`
- `refresh_expires_in`

## 2. Refresh token

```bash
curl -X POST "$CLAWTUNE_BASE_URL/token/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "installation_id": "<installation_id>",
    "refresh_token": "<refresh_token>",
    "channel": "openclaw",
    "user_ref": "demo-user-001"
  }'
```

## 3. 建议的 shell 环境变量

```bash
export CLAWTUNE_ACCESS_TOKEN="<access_token>"
export CLAWTUNE_INSTALLATION_ID="<installation_id>"
export CLAWTUNE_REFRESH_TOKEN="<refresh_token>"
```

## 4. 推荐配合脚本

- 自动确保凭证：

```bash
bash scripts/auth-bootstrap.sh ensure
```

- 打印当前本地 auth 状态：

```bash
bash scripts/auth-bootstrap.sh print
```
