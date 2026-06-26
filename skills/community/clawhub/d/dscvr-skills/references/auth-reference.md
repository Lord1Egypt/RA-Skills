# DSCVR API Authentication Reference

All product API endpoints (`/developer/v1/product/**`) require HMAC-SHA256 request signing.

## Required Headers

Every authenticated request must include these three headers:

| Header | Description | Example |
|---|---|---|
| `X-API-Key` | Your 16-character public API key | `your_api_key_here` |
| `X-Timestamp` | Current Unix timestamp in seconds | `1774338406` |
| `X-Signature` | HMAC-SHA256 hex digest | `08cffab6...e691de9d` |

## Signature Computation

The signature is computed as follows:

```
message  = "{api_key}:{timestamp}"
signature = HMAC-SHA256(secret_key, message).hexdigest()
```

### Python Implementation

```python
import hashlib
import hmac
import time

def compute_signature(secret_key: str, api_key: str, timestamp: str) -> str:
    message = f"{api_key}:{timestamp}".encode()
    return hmac.new(secret_key.encode(), message, hashlib.sha256).hexdigest()

# Generate headers
api_key = "your_api_key_here"
secret_key = "your_secret_key_here"
timestamp = str(int(time.time()))
signature = compute_signature(secret_key, api_key, timestamp)
```

### JavaScript Implementation

```javascript
const crypto = require('crypto');

function computeSignature(secretKey, apiKey, timestamp) {
  const message = `${apiKey}:${timestamp}`;
  return crypto.createHmac('sha256', secretKey).update(message).digest('hex');
}
```

## Verification Flow (Server-Side)

The server verifies requests in this order:

1. **Ban check** — If the API key is currently banned (in-memory, 1-minute duration), reject immediately with 403.
2. **Replay check** — If `|server_time - timestamp| > TIMESTAMP_TOLERANCE` (default: 300 seconds / 5 minutes), ban the key and reject with 401.
3. **DB lookup** — Query the database for the `secret_key` and `expire_time` associated with the `api_key`.
4. **Signature verify** — Compute the expected HMAC and compare using constant-time comparison (`hmac.compare_digest`).
5. **Expiry check** — If the subscription has expired (`expire_time <= now`), ban the key and reject with 401.

## Ban Policy

- Any authentication failure results in a **1-minute ban** for that API key.
- Bans are stored in-memory (not persisted across server restarts).
- During a ban, all requests with that API key are rejected with HTTP 403 immediately, without hitting the database.

## Timestamp Tolerance

- Default: **300 seconds** (5 minutes)
- Configurable via server's `TIMESTAMP_TOLERANCE` setting
- Ensure your system clock is synchronized (use NTP)

## Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| 401 on every request | Clock skew | Sync system clock with NTP |
| 401 after working fine | Subscription expired | Renew subscription on-chain |
| 403 for 60 seconds | Previous auth failure triggered ban | Wait 60 seconds, fix the root cause |
| Signature mismatch | Wrong secret key or encoding | Verify secret key, ensure UTF-8 encoding |
