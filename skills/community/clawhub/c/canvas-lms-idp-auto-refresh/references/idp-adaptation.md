# IDP Adaptation Guide

This reference covers how to adapt the login script to different institutional IDP systems.

## Supported IDP Pattern

The script targets a specific CAS/IDP flow common in Chinese higher education:

```
Browser → CAS Entry → IDP Portal (Vue SPA) → API calls (lck, authChainCode, publicKey)
  → RSA-encrypted auth → loginToken (JWT) → authnEngine redirect → SP callback → session
```

Key characteristics:
- IDP uses a Vue.js SPA at `/ac/` with hash-based routing
- Authentication methods queried via REST API (`/idp/authn/queryAuthMethods`)
- Password encrypted client-side with server-provided RSA public key (`/idp/authn/getJsPublicKey`)
- Login token submitted to authnEngine, which performs browser-redirect to SP
- SP consumes CAS ticket and establishes session cookies

## Step-by-Step Adaptation

### Step 1: Identify Your IDP URL Pattern

Visit your Canvas instance's login URL. Common patterns:

| University | Entry URL | IDP Base | Notes |
|---|---|---|---|
| Fudan | `https://elearning.fudan.edu.cn/login/cas` | `https://id.fudan.edu.cn` | Default config |
| Other Canvas+CAS | `https://canvas.example.edu/login/cas` | Varies | Check redirect chain |

Use `curl -vL <entry-url>` to trace the redirect chain and find the IDP base URL.

### Step 2: Test Basic Connectivity

```bash
ELEARNING_ENTRY_URL=https://your-canvas.example.edu/login/cas \
ELEARNING_IDP_BASE_URL=https://your-idp.example.edu \
ELEARNING_ENTITY_ID=https://your-canvas.example.edu \
python elearning_login.py --dry-run --debug
```

Check `debug_output/`:
- `entry_response.html` — should contain an `lck` value (format: `context_CAS_...`)
- `query_auth_methods.json` — should list `userAndPwd` as an auth module

### Step 3: Handle Differences

**Different auth module name**: If your IDP uses a different name than `userAndPwd`:
```python
# In auth_session.py → pick_auth_chain_code()
if module_code == "your_auth_module_name" and chain_code:
    return chain_code
```

**Different public key format**: The script already handles PEM, Base64-DER, and modulus+exponent (hex). If your IDP uses a different format, extend `parse_public_key_payload()`.

**Different login token location**: If the JWT is at a different JSON path, extend `extract_login_token()`.

**Different redirect mechanism**: If `authnEngine` uses a different redirect pattern, update `parse_authn_engine_handoff()`.

### Step 4: Token Purpose Convention

Set a meaningful token purpose in `.env`:
```
ELEARNING_TOKEN_PURPOSE="My Agent Auto Refresh"
```

This enables safe cleanup — old tokens with the same purpose are deleted, while manually created tokens are preserved.

### Step 5: Validate End-to-End

```bash
python elearning_login.py --cleanup-old-tokens --debug
```

Expected: `NEW_TOKEN=<value>` on stdout, all debug artifacts in `debug_output/`.

## Common IDP Variations

### SAML 2.0 (not CAS)

If your institution uses SAML 2.0 instead of CAS, the flow will be fundamentally different (SAMLRequest/SAMLResponse XML exchange). This script does **not** support SAML 2.0 directly.

### OAuth 2.0 / OIDC

If the login is OAuth-based (redirect to authorization endpoint), you can likely use direct OAuth flows instead of browser automation — much simpler and more reliable.

### Custom Captcha

Some IDPs embed CAPTCHA in the login form. The `requests`-based approach cannot handle this. You would need to:
1. Use a browser automation tool (Playwright/Selenium) instead
2. Or obtain a long-lived session token via manual login
