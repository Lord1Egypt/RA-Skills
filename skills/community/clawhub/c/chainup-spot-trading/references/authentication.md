# ChainUp OpenAPI V2 Authentication

This reference is based on the official documentation and FAQ:
- https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/bi-bi-jiao-yi
- https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/chang-jian-wen-ti

## Required Headers

- `Content-Type: application/json`
- `X-CH-APIKEY: <api_key>`
- `X-CH-SIGN: <signature>`
- `X-CH-TS: <timestamp_ms>`
- `admin-language: en_US`
- `User-Agent: chainup-spot/1.0.0 (Skill)`

## Signature Payload

Base format from the official FAQ:

`payload = timestamp + METHOD + requestPath + body`

Per the current integration rule set, matching the Postman pre-request script:

- `requestPath`: the path after removing `baseUrl` from the full URL; it may include `?query` and must not include the domain
- `timestamp`: millisecond timestamp string
- `METHOD`: uppercase HTTP method
- `GET`: `payload = timestamp + "GET" + requestPath` (do not append a body and do not append `"{}"`)
- `POST/PUT/PATCH`: `payload = timestamp + METHOD + requestPath + bodyStr`
- `bodyStr` (only for methods with a request body):
- If the original body exists and, after trimming whitespace, is not equal to `{}`, use the original body string
- Otherwise always use `"{}"`

General requirements:
- The JSON string used in a `POST` signature must match the actual request body exactly, including field names, order, and spaces
- If the endpoint requires query parameters to be signed, include the query string inside `requestPath` (for example `/sapi/v2/order?orderId=...&symbol=...`)
- `X-CH-SIGN` is `HMAC_SHA256(payload, secretKey)` encoded as lowercase hex

FAQ examples:
- `GET`: `1588591856950GET/sapi/v1/account`
- `POST`: `1588591856950POST/sapi/v1/order/test{"symbol":"BTCUSDT","price":"9300","volume":"1","side":"BUY","type":"LIMIT"}`

Postman-equivalent pseudocode:

```javascript
time = Date.now().toString()
requestPath = fullUrl.replace(baseUrl, "")
objStr = rawBody
if (method === "GET") {
  payload = time + method + requestPath
} else {
  bodyStr = (objStr && objStr.trim() !== "{}") ? objStr : "{}"
  payload = time + method + requestPath + bodyStr
}
sign = HmacSHA256(payload, secretKey).toHex()
headers: X-CH-SIGN, X-CH-APIKEY, X-CH-TS, admin-language
```

## HMAC SHA256 + HEX

For `openapi.coobit.cc`, the currently working signature encoding is hexadecimal (HEX):

```bash
SIGN=$(printf '%s' "$PAYLOAD" \
  | openssl dgst -sha256 -hmac "$SECRET_KEY" \
  | awk '{print $2}')
```

## Curl Examples

### GET /sapi/v1/account

```bash
TS=$(date +%s%3N)
METHOD="GET"
PATH="/sapi/v1/account"
PAYLOAD="${TS}${METHOD}${PATH}"
SIGN=$(printf '%s' "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET_KEY" | awk '{print $2}')

curl -sS "${BASE_URL}${PATH}" \
  -H "Content-Type: application/json" \
  -H "X-CH-APIKEY: ${API_KEY}" \
  -H "X-CH-TS: ${TS}" \
  -H "X-CH-SIGN: ${SIGN}" \
  -H "admin-language: en_US" \
  -H "User-Agent: chainup-spot/1.0.0 (Skill)"
```

### POST /sapi/v2/order (MARKET SELL)

```bash
TS=$(date +%s%3N)
METHOD="POST"
PATH="/sapi/v2/order"
BODY='{"symbol":"BTC/USDT","volume":"0.001","side":"SELL","type":"MARKET"}'
PAYLOAD="${TS}${METHOD}${PATH}${BODY}"
SIGN=$(printf '%s' "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET_KEY" | awk '{print $2}')

curl -sS -X POST "${BASE_URL}${PATH}" \
  -H "Content-Type: application/json" \
  -H "X-CH-APIKEY: ${API_KEY}" \
  -H "X-CH-TS: ${TS}" \
  -H "X-CH-SIGN: ${SIGN}" \
  -H "admin-language: en_US" \
  -H "User-Agent: chainup-spot/1.0.0 (Skill)" \
  -d "$BODY"
```

### GET /sapi/v2/order (Query Order)

```bash
TS=$(date +%s%3N)
METHOD="GET"
PATH="/sapi/v2/order"
QUERY="orderId=3181965742962937069&symbol=ETH%2FUSDT"
PAYLOAD="${TS}${METHOD}${PATH}?${QUERY}"
SIGN=$(printf '%s' "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET_KEY" | awk '{print $2}')

curl -sS "${BASE_URL}${PATH}?${QUERY}" \
  -H "Content-Type: application/json" \
  -H "X-CH-APIKEY: ${API_KEY}" \
  -H "X-CH-TS: ${TS}" \
  -H "X-CH-SIGN: ${SIGN}" \
  -H "admin-language: en_US" \
  -H "User-Agent: chainup-spot/1.0.0 (Skill)"
```

## Notes

- The server default receive window is 5000ms. It can be customized with the business parameter `recvwindow`.
- If the server reports an invalid timestamp, verify the local system clock first and then retry.
- If signature verification fails, check these points first:
- Whether the concatenation order is exact
- Whether `requestPath` incorrectly includes the domain (it should not)
- Whether `GET` incorrectly appended a body or `"{}"` (`GET` should sign only `timestamp + GET + requestPath`)
- Whether an empty non-`GET` body was signed as `"{}"`
- Whether `GET` should include `?query` inside the signed path
- Whether the signed `POST` body matches the actual JSON sent exactly
- Whether the output encoding matches what the gateway expects (HEX or Base64)
