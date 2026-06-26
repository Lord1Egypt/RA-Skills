# Credentials Guard Reference

## API (chanjing-openapi.yaml)

### Get Access Token

| Item | Value |
|------|--------|
| Method | POST |
| URL | `https://open-api.chanjing.cc/open/v1/access_token` |
| Content-Type | application/json |

**Request body** (dto.OpenAccessTokenReq):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| app_id | string | Yes | Access Key (AK) |
| secret_key | string | Yes | Secret Key (SK) |

**Response** (success code=0):

| Field | Type | Description |
|-------|------|-------------|
| code | int | 0 = success |
| msg | string | Message |
| data.access_token | string | API credential |
| data.expire_in | int | Unix timestamp, token expiry |

**Error codes**:

| code | Description |
|------|-------------|
| 0 | Success |
| 400 | Invalid parameter format |
| 40000 | Parameter error |
| 50000 | Internal error |

## Credential storage format

app_id/secret_key are read from project `.env`. Path and format follow **`scripts/chanjing_config.py`**.

File path: `skills/chanjing-content-creation-skill/.env` (default; override with env `CHANJING_ENV_FILE`)

```bash
CHANJING_APP_ID=<app_id>
CHANJING_SECRET_KEY=<secret_key>
```
Token 不写入 `.env`。可选地由进程环境提供 `CHANJING_ACCESS_TOKEN` 与 `CHANJING_TOKEN_EXPIRE_IN`，否则按需请求并在进程内短时复用。

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| CHANJING_ENV_FILE | Credentials file path | skills/chanjing-content-creation-skill/.env |
| CHANJING_API_BASE | API base URL | https://open-api.chanjing.cc |

## Login and obtaining keys

- Sign up / Login: https://www.chanjing.cc/openapi/login
- Docs: https://doc.chanjing.cc
