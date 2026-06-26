# Aster Spot Authentication

All trading endpoints require HMAC SHA256 signed requests.

## Base URLs

| Environment | URL |
|-------------|-----|
| Mainnet | https://sapi.asterdex.com |

## Required Headers

```
X-MBX-APIKEY: your_api_key
```

The API key is case-sensitive and must be included in the `X-MBX-APIKEY` header for all authenticated requests.

## Authentication Types

| Type | Requirements |
|------|-------------|
| NONE | No authentication needed |
| TRADE | Valid API-Key and signature required |
| USER_DATA | Valid API-Key and signature required |
| USER_STREAM | Valid API-Key required |
| MARKET_DATA | Valid API-Key required |

## Signing Process (HMAC SHA256)

### Step 1: Build Query String

Include all parameters plus `timestamp` (current Unix time in milliseconds):

```
symbol=BTCUSDT&side=BUY&type=MARKET&quantity=0.001&timestamp=1234567890123
```

**Optional:** Add `recvWindow` (default 5000ms) for timestamp tolerance.

### Step 2: Generate Signature

Create HMAC SHA256 signature of the full parameter string using your secret key:

```bash
# Example using openssl
echo -n "symbol=BTCUSDT&side=BUY&type=MARKET&quantity=0.001&timestamp=1234567890123" | \
  openssl dgst -sha256 -hmac "your_secret_key"
```

The signature is generated from the concatenation of all query string and request body parameters.

### Step 3: Append Signature

Add signature parameter to the request:

```
symbol=BTCUSDT&side=BUY&type=MARKET&quantity=0.001&timestamp=1234567890123&signature=abc123...
```

## Timestamp / recvWindow

- Signed endpoints must include the `timestamp` parameter (Unix timestamp in milliseconds)
- Server accepts timestamps within 5,000 milliseconds of server time by default
- Adjustable via `recvWindow` parameter (recommended under 5 seconds, maximum 60 seconds)

## Complete Example (bash/curl)

```bash
#!/bin/bash
API_KEY="your_api_key"
SECRET_KEY="your_secret_key"
BASE_URL="https://sapi.asterdex.com"

# Get current timestamp
TIMESTAMP=$(date +%s000)

# Build query string (without signature)
QUERY="symbol=BTCUSDT&side=BUY&type=MARKET&quantity=0.001&timestamp=${TIMESTAMP}"

# Generate signature
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET_KEY" | cut -d' ' -f2)

# Make request
curl -X POST "${BASE_URL}/sapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}"
```

## Complete Example (Python)

```python
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

API_KEY = "your_api_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://sapi.asterdex.com"

def sign_request(params: dict) -> str:
    """Generate HMAC SHA256 signature for request parameters."""
    query_string = urlencode(params)
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return signature

# Example: Place a market order
params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": "0.001",
    "timestamp": int(time.time() * 1000),
}

signature = sign_request(params)
params["signature"] = signature

headers = {
    "X-MBX-APIKEY": API_KEY,
}

response = requests.post(
    f"{BASE_URL}/sapi/v1/order",
    headers=headers,
    params=params,
)
print(response.json())
```

## API Key Creation Process

Aster Spot API keys are created using an EVM wallet signature flow:

1. **Get Nonce:** Call the `getNonce` endpoint to receive a signing nonce
2. **Sign with Wallet:** Sign the nonce message with your EVM wallet
3. **Create API Key:** Call `createApiKey` with the wallet signature to receive your API key and secret

Store the API secret securely -- it is only shown once during creation.

## Security Notes

* Never reveal your API key or secret to anyone
* Access restrictions are based on IP, not API Key
* Use IP whitelist restrictions where possible
* Enable only required permissions
* Use WebSocket connections to reduce rate-limit pressure
* TESTUSDT or any symbols starting with TEST are for Aster's internal testing only
