# Binance Auth and Signing

Binance Spot uses security types per endpoint: `NONE`, `TRADE`, `USER_DATA`, and `USER_STREAM`.
Most non-public methods are `SIGNED` and require `timestamp` plus signature.

## HMAC-SHA256 Signing (common path)

1. Build query parameters.
2. Include `timestamp` in milliseconds.
3. Sort params by name for deterministic payloads.
4. Sign the exact payload string with HMAC-SHA256 and API secret.
5. Send `X-MBX-APIKEY` header.

```bash
sign_hmac() {
  local payload="$1"
  printf "%s" "$payload" | openssl dgst -sha256 -hmac "$BINANCE_API_SECRET" | sed 's/^.* //'
}
```

## Minimal signed request template

```bash
BASE="${BINANCE_BASE_URL:-https://api.binance.com}"
TS=$(curl -s "$BASE/api/v3/time" | jq -r '.serverTime')
QS="symbol=BTCUSDT&timestamp=$TS&recvWindow=5000"
SIG=$(sign_hmac "$QS")

curl -s -H "X-MBX-APIKEY: $BINANCE_API_KEY" \
  "$BASE/api/v3/order/test?$QS&signature=$SIG"
```

## RSA and Ed25519 keys

Spot supports HMAC, RSA, and Ed25519 API keys for signed methods.
If using RSA or Ed25519, sign according to Binance key type requirements and keep key material outside repositories.

## RecvWindow and timing

- Keep `recvWindow` tight (for example, 5000).
- Use server time, not local clock, for `timestamp`.
- If `-1021` appears, resync time before retrying.

## WebSocket API signing

WebSocket API signed methods also require sorted params, `apiKey`, `timestamp`, and signature.
Use the same canonicalization rule as REST to avoid mismatched signatures.
