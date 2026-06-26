# Canvas LMS IDP Auto Token Refresh

Automatically refresh Canvas LMS API tokens by replaying institutional IDP (CAS/SAML) login with RSA-encrypted credentials.

## Overview

Many universities deploy Canvas LMS behind institutional SSO (CAS/SAML). API tokens generated through Canvas settings may be invalidated by the SSO layer on a daily or session basis. This project automates the full login chain to programmatically create fresh Canvas API tokens without manual intervention.

## How It Works

```
Entry URL → CAS/IDP (lck + authChainCode) → RSA encrypt password → authExecute
  → loginToken (JWT) → authnEngine → SSO ticket → Canvas session → create API token
  → (optional) delete old tokens by purpose → output NEW_TOKEN=xxx
```

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # or: .venv\Scripts\activate (Windows)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env — fill in ELEARNING_USERNAME and ELEARNING_PASSWORD

# 4. Test (dry-run — only fetches public key, no login)
python elearning_login.py --dry-run --debug

# 5. Full flow: login → create token → cleanup old tokens
python elearning_login.py --cleanup-old-tokens
```

On success: `NEW_TOKEN=<token_value>` is printed to stdout.

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `ELEARNING_USERNAME` | ✅ | — | Student/staff ID |
| `ELEARNING_PASSWORD` | ✅ | — | Password |
| `ELEARNING_ENTRY_URL` | | `https://elearning.fudan.edu.cn/login/cas` | CAS entry point |
| `ELEARNING_IDP_BASE_URL` | | `https://id.fudan.edu.cn` | IDP base URL |
| `ELEARNING_ENTITY_ID` | | `https://elearning.fudan.edu.cn` | Service provider entity ID |
| `ELEARNING_TOKEN_PURPOSE` | | `OpenClaw Auto Refresh Token` | Label for created tokens |
| `ELEARNING_CLEANUP_OLD_TOKENS` | | `0` | Auto-delete old tokens with same purpose |
| `ELEARNING_TIMEOUT_SECONDS` | | `20` | Request timeout in seconds |

## CLI Options

```
--debug               Verbose HTTP logs + save debug artifacts to debug_output/
--dry-run             Only test up to public key fetch (no actual login)
--skip-token          Login but skip token creation
--cleanup-old-tokens  Delete old tokens matching purpose after creating new one
--cleanup-purpose     Override which purpose to match for cleanup
--cleanup-dry-run     Preview which tokens would be deleted without deleting
--dump-dir            Custom debug output directory (default: debug_output/)
```

## Integrating with Your Agent/Tool

Implement a lazy-refresh pattern:

1. Read saved token from file
2. Validate with `GET /api/v1/users/self` (check HTTP status only)
3. If 200 → use token for API calls
4. If 401 → run this script, capture `NEW_TOKEN=`, save to file, retry
5. If script fails → alert user (password changed, CAPTCHA triggered, etc.)

## Adapting to Other Institutions

The IDP flow is based on a common CAS pattern used by many Chinese universities:

1. Change URLs in `.env` (`ELEARNING_ENTRY_URL`, `ELEARNING_IDP_BASE_URL`, `ELEARNING_ENTITY_ID`)
2. Test with `--dry-run --debug` to verify lck/authChainCode extraction
3. If auth methods differ: modify `pick_auth_chain_code()` in `auth_session.py`
4. If encryption differs: modify `encrypt_password_rsa()` and `parse_public_key_payload()`

Tested with: **Fudan University** (`id.fudan.edu.cn` → `elearning.fudan.edu.cn`).

## Troubleshooting

Run with `--debug` to save artifacts to `debug_output/`:

| Symptom | Check |
|---|---|
| `未能从入口响应中解析到 lck` | `entry_response.html` — look for `context_CAS_...` |
| `queryAuthMethods 未找到 userAndPwd` | `query_auth_methods.json` — check `moduleCode` |
| `未从 authExecute 提取到 loginToken` | `auth_execute.json` — check `code`/`message` |
| `未拿到关键会话 Cookie` | Check for CAPTCHA, verify credentials |
| Token API 401/422 | `cookies.txt` for `_csrf_token` / `_normandy_session` |
| Cleanup fails | `cleanup_summary.json` for `failed` entries |

## Security Notes

- `.env` contains credentials — **never commit to git**
- `debug_output/` may contain session data — **sanitize before sharing**
- Password encrypted with server-provided RSA public key (PKCS1v1_5)
- Tokens created with purpose label for safe lifecycle management

## Known Limitations

- **CAPTCHA/Rate-limiting**: Cannot solve human verification — manual intervention required
- **MFA/2FA**: Not supported (requires interactive flow)
- **IDP interface changes**: May break if JSON fields or HTML structure change
- **SAML 2.0 (non-CAS)**: Not directly supported

## License

MIT

## Acknowledgments

Developed for automating Canvas LMS token lifecycle at Fudan University.
Also available as an [OpenClaw skill](https://clawhub.com) (`canvas-lms-idp-auto-refresh`).
