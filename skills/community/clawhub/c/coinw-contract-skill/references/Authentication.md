# Authentication & Base URL

## Base URL
- Spot: `https://api.coinw.com`
- Futures: `https://api.coinw.com`

## Private Authentication (Futures/Contract: HMAC-SHA256)
CoinW contract private endpoints use header-based signature auth with `api_key`, `timestamp`, and `sign`.

1. Build `timestamp` in milliseconds (for example `1713945600123`).
2. Build the signing payload:
   - GET: `{timestamp}{METHOD}{api_url}?{query_string}` (omit `?` when query is empty)
   - POST/PUT/DELETE: `{timestamp}{METHOD}{api_url}{json_body}`
3. Compute signature with HMAC-SHA256 using `secret_key`.
4. Base64-encode the HMAC digest as `sign`.
5. Send headers:
   - `api_key: $COINW_API_KEY`
   - `timestamp: <ms timestamp>`
   - `sign: <base64 hmac signature>`
   - `Content-type: application/json` for POST/PUT/DELETE

## Important
- Contract and Spot use different signing algorithms and payload formats.
- Do not reuse Spot MD5 signing for Contract endpoints.
- Spot/Common Account endpoints use MD5 uppercase signing (see Spot/Auth reference).

See examples in each skill for a minimal signing template.
