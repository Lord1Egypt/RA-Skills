# Authentication

TIDY uses Bearer token authentication. Get a token by signing up or logging in, then include it in all subsequent requests.

## Sign Up (New Account)

```bash
curl -X POST https://public-api.tidy.com/api/v2/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "password": "secret123"
  }'
```

**Response:**
```json
{ "token": "abc123...", "customer_id": 12345 }
```

## Log In (Existing Account)

```bash
curl -X POST https://public-api.tidy.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "secret123"
  }'
```

**Response:**
```json
{ "token": "abc123...", "customer_id": 12345 }
```

## Using the Token

Include the token in the `Authorization` header for all authenticated requests:

```
Authorization: Bearer abc123...
```

## Token Storage

**Environment variable (recommended):**

```bash
export TIDY_API_TOKEN="abc123..."
```

The CLI (`tidy-request`) reads `TIDY_API_TOKEN` automatically. If not set, credentials are stored in `~/.config/tidy/credentials` after running `tidy-request login` or `tidy-request signup`.

## Token Lifecycle

- Tokens **do not expire**
- Logging in again returns a new token (previous tokens remain valid)
- Store your token securely — treat it like a password

## MCP Authentication

When using the MCP server, call the `login` or `signup` tool first. The returned token is automatically used for subsequent tool calls in the same session.

```
login(email: "jane@example.com", password: "secret123")
  → { token: "abc123...", customer_id: 12345, message: "Authenticated successfully..." }
```

## Error Responses

| HTTP Status | Error Type | When |
|---|---|---|
| 401 | `authentication_error` | Bad credentials or missing/invalid token |
| 409 | `conflict` | Account already exists (signup) |
| 422 | `invalid_request_error` | Missing email or password |
