# Authentication & Base URL

## Base URL
- Spot: `https://api.coinw.com`
- Futures: `https://api.coinw.com`

## Private Authentication (MD5 signature)
CoinW private endpoints require an `api_key` and an `sign` parameter.

1. Include `api_key` and request parameters.
2. Sort all parameters by key (ascending).
3. Build query string `k1=v1&k2=v2...`.
4. Append `&secret_key=$COINW_SECRET_KEY`.
5. Compute MD5 hash, output in UPPERCASE.
6. Use it as `sign` in the request.

See examples in each skill for a minimal signing template.
