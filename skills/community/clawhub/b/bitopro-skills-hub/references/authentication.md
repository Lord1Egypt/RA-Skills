# BitoPro API Authentication

## Overview

BitoPro uses **HMAC-SHA384** signature-based authentication for all private endpoints. Every authenticated request must include custom HTTP headers.

## Required Headers

| Header | Description | When to Include |
|--------|-------------|-----------------|
| `X-BITOPRO-APIKEY` | Your API Key | All authenticated requests |
| `X-BITOPRO-PAYLOAD` | Base64-encoded JSON payload | All authenticated requests |
| `X-BITOPRO-SIGNATURE` | HMAC-SHA384 hex digest (keyed with API Secret) | All authenticated requests |

> All three headers are required for every authenticated request (GET, POST, PUT, DELETE).

## Environment Variables

All three are required:

```
BITOPRO_API_KEY=your_api_key
BITOPRO_API_SECRET=your_api_secret
BITOPRO_EMAIL=your_registered_email
```

## Payload Construction Rules (Critical Difference)

### GET / DELETE Requests

The payload body is always `identity` (email) + `nonce`:

```json
{
  "identity": "user@example.com",
  "nonce": 1554380909131
}
```

### POST / PUT Requests

The payload body is the actual request parameters plus `nonce` (**no `identity` field**):

```json
{
  "action": "BUY",
  "amount": "0.001",
  "price": "3000000",
  "type": "LIMIT",
  "timestamp": 1554380909131,
  "nonce": 1554380909131
}
```

> **`nonce`**: A monotonically increasing integer. Use the current Unix timestamp in milliseconds.

## Signing Process

```
1. Build the payload object based on HTTP method:
   - GET/DELETE → { identity: email, nonce }
   - POST/PUT  → { ...requestBody, nonce }

2. encoded_payload = Base64Encode(JSON.stringify(payload_object))

3. signature = HMAC-SHA384(encoded_payload, API_SECRET).hexdigest()

4. Attach headers:
   - X-BITOPRO-APIKEY:     API_KEY
   - X-BITOPRO-PAYLOAD:    encoded_payload
   - X-BITOPRO-SIGNATURE:  signature
```

## Code Examples

### Python

```python
import hmac
import hashlib
import base64
import json
import time


def build_headers(method: str, api_key: str, api_secret: str, email: str, body: dict = None) -> dict:
    """
    Build authenticated headers for BitoPro API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        api_key: API key (read from $BITOPRO_API_KEY env var)
        api_secret: API secret (read from $BITOPRO_API_SECRET env var)
        email: Account email (read from $BITOPRO_EMAIL env var)
        body: Request body dict (for POST/PUT only)
    """
    nonce = int(time.time() * 1000)

    # GET/DELETE use identity + nonce; POST/PUT use actual body + nonce
    if method.upper() in ('GET', 'DELETE'):
        payload_obj = {"identity": email, "nonce": nonce}
    else:
        payload_obj = {**(body or {}), "nonce": nonce}

    payload = base64.b64encode(
        json.dumps(payload_obj).encode('utf-8')
    ).decode('utf-8')

    signature = hmac.new(
        api_secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha384
    ).hexdigest()

    headers = {
        'X-BITOPRO-APIKEY': api_key,
        'X-BITOPRO-PAYLOAD': payload,
        'X-BITOPRO-SIGNATURE': signature,
        'Content-Type': 'application/json',
    }

    return headers
```

#### Python Usage Examples

```python
import requests

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
EMAIL = "your@email.com"
BASE_URL = "https://api.bitopro.com/v3"

# GET example: query account balance
headers = build_headers("GET", API_KEY, API_SECRET, EMAIL)
resp = requests.get(f"{BASE_URL}/accounts/balance", headers=headers)
print(resp.json())

# POST example: create an order
nonce = int(time.time() * 1000)
order_body = {
    "action": "BUY",
    "amount": "0.001",
    "price": "2800000",
    "type": "LIMIT",
    "timestamp": nonce,
    "nonce": nonce,  # nonce must be in both payload AND request body
}
headers = build_headers("POST", API_KEY, API_SECRET, EMAIL, body=order_body)
resp = requests.post(f"{BASE_URL}/orders/btc_twd", headers=headers, json=order_body)
print(resp.json())

# DELETE example: cancel an order
headers = build_headers("DELETE", API_KEY, API_SECRET, EMAIL)
resp = requests.delete(f"{BASE_URL}/orders/btc_twd/1234567890", headers=headers)
print(resp.json())
```

### Go

```go
package bitopro

import (
    "crypto/hmac"
    "crypto/sha512"
    "encoding/base64"
    "encoding/hex"
    "encoding/json"
    "net/http"
    "time"
)

// BuildHeaders creates authenticated headers for BitoPro API.
func BuildHeaders(method, apiKey, apiSecret, email string, body map[string]interface{}) http.Header {
    nonce := time.Now().UnixMilli()

    var payloadObj map[string]interface{}

    if method == http.MethodGet || method == http.MethodDelete {
        // GET/DELETE: identity + nonce
        payloadObj = map[string]interface{}{
            "identity": email,
            "nonce":    nonce,
        }
    } else {
        // POST/PUT: actual body + nonce
        payloadObj = make(map[string]interface{})
        for k, v := range body {
            payloadObj[k] = v
        }
        payloadObj["nonce"] = nonce
    }

    payloadJSON, _ := json.Marshal(payloadObj)
    encodedPayload := base64.StdEncoding.EncodeToString(payloadJSON)

    mac := hmac.New(sha512.New384, []byte(apiSecret))
    mac.Write([]byte(encodedPayload))
    signature := hex.EncodeToString(mac.Sum(nil))

    headers := http.Header{}
    headers.Set("X-BITOPRO-APIKEY", apiKey)
    headers.Set("X-BITOPRO-SIGNATURE", signature)
    headers.Set("Content-Type", "application/json")

    headers.Set("X-BITOPRO-PAYLOAD", encodedPayload)

    return headers
}
```

#### Go Usage Examples

```go
package main

import (
    "fmt"
    "io"
    "net/http"
)

func main() {
    apiKey := "your_api_key"
    apiSecret := "your_api_secret"
    email := "your@email.com"
    baseURL := "https://api.bitopro.com/v3"

    // GET: query account balance
    headers := BuildHeaders(http.MethodGet, apiKey, apiSecret, email, nil)
    req, _ := http.NewRequest("GET", baseURL+"/accounts/balance", nil)
    req.Header = headers
    resp, _ := http.DefaultClient.Do(req)
    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))

    // DELETE: cancel an order
    headers = BuildHeaders(http.MethodDelete, apiKey, apiSecret, email, nil)
    req, _ = http.NewRequest("DELETE", baseURL+"/orders/btc_twd/1234567890", nil)
    req.Header = headers
    resp, _ = http.DefaultClient.Do(req)
    body, _ = io.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```

## Rate Limits

| Endpoint Type | Limit |
|---------------|-------|
| Open API (Public) | 600 requests / min / IP |
| Auth API (Private) | 600 requests / min / IP + 600 requests / min / UID |
| Create Order | 1200 requests / min / UID |
| Create Batch Orders | 90 requests / min / IP & UID |
| Cancel Order | 900 requests / min / UID |
| Cancel Batch Orders | 2 requests / sec / IP |
| Cancel All Orders | 1 request / sec / IP & UID |
| Open Orders | 5 requests / sec / UID |
| Create Withdraw | 60 requests / min / IP |

## Common Errors

| HTTP Code | Meaning |
|-----------|---------|
| 401 | Invalid API key or signature |
| 403 | Permission denied (check API key permission settings) |
| 429 | Rate limit exceeded |

## Important Notes

- The `nonce` must be **monotonically increasing**. Using `int(time.time() * 1000)` (milliseconds) is recommended.
- API keys can be configured with **read-only** or **trade** permissions in the BitoPro dashboard.
- **Never** expose your `API_SECRET` in client-side code or public repositories.
- All authenticated requests require all three headers: `X-BITOPRO-APIKEY`, `X-BITOPRO-PAYLOAD`, `X-BITOPRO-SIGNATURE`.
