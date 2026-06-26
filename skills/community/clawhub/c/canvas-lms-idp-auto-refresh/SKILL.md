---
name: canvas-lms-idp-auto-refresh
description: Auto-refresh Canvas LMS API tokens via institutional IDP (CAS/SAML) login. Use when: (1) Canvas API returns 401 and you need to re-authenticate, (2) setting up automated token lifecycle for any Canvas LMS deployment behind an institutional SSO (especially Chinese universities using id.fudan.edu.cn style IDP), (3) user asks about "canvas token expired", "自动刷新token", "elearning login", "IDP登录". Handles RSA-encrypted password auth, SSO ticket exchange, token creation and old token cleanup.
---

# Canvas LMS — IDP Auto Token Refresh

Automate Canvas API token refresh by replaying institutional IDP login (CAS/SAML) with RSA-encrypted credentials.

## How It Works

```
Entry URL → CAS/IDP (lck + authChainCode) → RSA encrypt password → authExecute
  → loginToken (JWT) → authnEngine → SSO ticket → Canvas session → create API token
  → (optional) delete old tokens by purpose → output NEW_TOKEN=xxx
```

The script handles the full IDP chain: cookie juggling, JavaScript-redirect handoff, CSRF extraction, and Canvas API token CRUD.

## Quick Start

### 1. Install Dependencies

```bash
cd scripts/
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependencies: `requests`, `beautifulsoup4`, `pycryptodome`, `python-dotenv`.

### 2. Configure Credentials

Copy `.env.example` to `.env` and fill in:

```bash
cp scripts/.env.example scripts/.env
```

Required fields:
- `ELEARNING_USERNAME` — student/staff ID
- `ELEARNING_PASSWORD` — password

Optional (defaults to Fudan eLearning):
- `ELEARNING_ENTRY_URL` — CAS entry point
- `ELEARNING_IDP_BASE_URL` — IDP base URL
- `ELEARNING_ENTITY_ID` — SP entity ID
- `ELEARNING_TOKEN_PURPOSE` — label for created tokens (default: "OpenClaw Auto Refresh Token")
- `ELEARNING_CLEANUP_OLD_TOKENS` — auto-delete old tokens with same purpose (default: false)

### 3. Run

```bash
# Full flow: login → create token → cleanup old tokens
cd scripts && .venv/bin/python elearning_login.py --cleanup-old-tokens

# Debug mode (verbose HTTP logs + save debug artifacts)
cd scripts && .venv/bin/python elearning_login.py --debug --cleanup-old-tokens

# Dry-run: only test up to public key fetch (no login)
cd scripts && .venv/bin/python elearning_login.py --dry-run --debug
```

On success, the script prints `NEW_TOKEN=<token_value>` to stdout.

### 4. Integrate with Token Lazy-Loading

For agents that call Canvas API, implement a lazy-refresh pattern:

1. Read saved token from file
2. Validate with `GET /api/v1/users/self` — check HTTP status only (don't read body)
3. If 200 → use token
4. If 401 → run refresh script, capture `NEW_TOKEN=`, save to file, retry
5. If refresh also fails → alert user (password changed, CAPTCHA triggered, etc.)

**Key rules:**
- Validate once per session, not on every API call
- Only re-validate on explicit 401 responses
- Don't log or expose raw token values
- The refresh takes ~2-3 seconds, run silently

## Security

- `.env` contains credentials — **never commit to git** (`.env` is gitignored by default)
- `debug_output/` may contain session cookies and encrypted payloads — **sanitize before sharing**
- The script uses PKCS1v1_5 RSA encryption for password transport (matching the IDP's JS frontend)
- Tokens are created with a purpose label for lifecycle management
- Old tokens with matching purpose can be auto-deleted to avoid accumulation

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| CAPTCHA/rate-limiting | Script cannot solve human verification | Alert user, manual intervention needed |
| MFA/2FA | Requires interactive flow not supported by `requests` | Not supported; alert user |
| IDP interface changes | JSON field names or HTML structure may change | Debug output (`--debug`) captures raw responses for diagnosis |
| Public key format changes | Script supports PEM, Base64-DER, modulus+exponent | If new format appears, extend `parse_public_key_payload()` |

## Troubleshooting

Run with `--debug` to save artifacts to `debug_output/`:

| Symptom | Check |
|---|---|
| `未能从入口响应中解析到 lck` | `debug_output/entry_response.html` — look for `context_CAS_...` |
| `queryAuthMethods 未找到 userAndPwd` | `debug_output/query_auth_methods.json` — check `moduleCode` field |
| `未从 authExecute 提取到 loginToken` | `debug_output/auth_execute.json` — check `code`/`message` |
| `未拿到关键会话 Cookie` | Check `auth_execute.json` for errors, `authn_engine_response.html` for CAPTCHA |
| Token API returns 401/422 | `debug_output/cookies.txt` for `_csrf_token` / `_normandy_session` |
| Cleanup fails | `debug_output/cleanup_summary.json` for `failed` entries |

## Adapting to Other Institutions

The IDP flow is based on a common CAS/SAML pattern used by many Chinese universities. To adapt:

1. **Change URLs** in `.env`: `ELEARNING_ENTRY_URL`, `ELEARNING_IDP_BASE_URL`, `ELEARNING_ENTITY_ID`
2. **Test with `--dry-run`** first to verify `lck`/`authChainCode` extraction
3. **If IDP uses different auth methods**: modify `pick_auth_chain_code()` in `auth_session.py`
4. **If password encryption differs**: modify `encrypt_password_rsa()` and `parse_public_key_payload()`

Tested with: Fudan University (id.fudan.edu.cn → elearning.fudan.edu.cn).
