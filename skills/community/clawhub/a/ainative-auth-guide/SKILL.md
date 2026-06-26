---
name: ainative-auth-guide
description: Implement authentication for AINative APIs. Use when (1) Choosing between API key and JWT auth, (2) Registering/logging in users, (3) Refreshing tokens, (4) Implementing OAuth2 (LinkedIn/GitHub), (5) Using API keys for server-side or agent use. Covers email/password, OAuth2 social login, API key management, and middleware patterns. Closes #1519.
---

# AINative Authentication Guide

## Auth Methods

| Method | Use Case | Header |
|--------|----------|--------|
| API Key | Server-side, agents, SDKs, MCP tools | `X-API-Key: ak_...` |
| Bearer JWT | User sessions, web apps | `Authorization: Bearer <token>` |
| OAuth2 | Social login (LinkedIn, GitHub) | Standard OAuth2 flow |

## API Key Auth (Simplest)

Get a key via `npx zerodb init` or from the dashboard.

```python
import requests

response = requests.get(
    "https://api.ainative.studio/api/v1/public/credits/balance",
    headers={"X-API-Key": "ak_your_key"}
)
```

```typescript
const res = await fetch("https://api.ainative.studio/api/v1/public/credits/balance", {
  headers: { "X-API-Key": "ak_your_key" }
});
```

## Email/Password Registration & Login

```python
# Register
resp = requests.post(
    "https://api.ainative.studio/api/v1/auth/register",
    json={"email": "user@example.com", "password": "securepass", "name": "Alice"}
)
token = resp.json()["access_token"]

# Login
resp = requests.post(
    "https://api.ainative.studio/api/v1/auth/login",
    json={"email": "user@example.com", "password": "securepass"}
)
access_token = resp.json()["access_token"]
refresh_token = resp.json()["refresh_token"]
```

## JWT Usage

```python
headers = {"Authorization": f"Bearer {access_token}"}
me = requests.get("https://api.ainative.studio/api/v1/users/me", headers=headers).json()
```

## Token Refresh

```python
resp = requests.post(
    "https://api.ainative.studio/api/v1/auth/refresh",
    json={"refresh_token": refresh_token}
)
new_access_token = resp.json()["access_token"]
```

## Logout

```python
requests.post(
    "https://api.ainative.studio/api/v1/auth/logout",
    headers={"Authorization": f"Bearer {access_token}"}
)
```

## OAuth2 Social Login

```python
# LinkedIn
resp = requests.post(
    "https://api.ainative.studio/api/v1/auth/linkedin/callback",
    json={"code": oauth_code, "redirect_uri": "https://yourapp.com/callback"}
)

# GitHub
resp = requests.post(
    "https://api.ainative.studio/api/v1/auth/github/callback",
    json={"code": oauth_code, "redirect_uri": "https://yourapp.com/callback"}
)
token = resp.json()["access_token"]
```

## Next.js Middleware

```typescript
// middleware.ts
import { createMiddleware } from '@ainative/next-sdk/middleware';

export const middleware = createMiddleware({
  apiKey: process.env.AINATIVE_API_KEY!,
  protectedPaths: ['/dashboard', '/api/protected'],
  loginPath: '/login',
});
```

## Password Reset

```python
# Request reset email
requests.post("https://api.ainative.studio/api/v1/auth/forgot-password",
    json={"email": "user@example.com"})

# Set new password with token from email
requests.post("https://api.ainative.studio/api/v1/auth/reset-password",
    json={"token": "reset_token_from_email", "new_password": "newpassword"})
```

## Auth Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Create account |
| `/api/v1/auth/login` | POST | Email/password → JWT |
| `/api/v1/auth/logout` | POST | Invalidate session |
| `/api/v1/auth/refresh` | POST | Refresh access token |
| `/api/v1/users/me` | GET | Current user profile |
| `/api/v1/auth/verify-email` | POST | Verify email address |
| `/api/v1/auth/forgot-password` | POST | Send reset email |
| `/api/v1/auth/reset-password` | POST | Apply new password |
| `/api/v1/auth/linkedin/callback` | POST | LinkedIn OAuth2 |
| `/api/v1/auth/github/callback` | POST | GitHub OAuth2 |

## Error Codes

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing token/key |
| 403 | Valid auth, insufficient permissions |
| 409 | Email already registered |

## References

- `src/backend/app/api/v1/endpoints/auth.py` — Auth endpoint implementation
- `packages/sdks/nextjs/src/middleware/` — Next.js auth middleware
- `docs/guides/AUTHENTICATION.md` — Full authentication guide
