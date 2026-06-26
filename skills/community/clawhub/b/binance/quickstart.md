# Binance Quickstart

Use this flow to validate connectivity and signing with minimal risk.

## 1) Environment

```bash
export BINANCE_API_KEY="..."
export BINANCE_API_SECRET="..."
export BINANCE_BASE_URL="https://testnet.binance.vision"
```

## 2) Public health checks

```bash
curl -s "$BINANCE_BASE_URL/api/v3/ping"
curl -s "$BINANCE_BASE_URL/api/v3/time" | jq
curl -s "$BINANCE_BASE_URL/api/v3/exchangeInfo?symbol=BTCUSDT" | jq '.symbols[0].filters'
```

## 3) Signed account check

```bash
TS=$(curl -s "$BINANCE_BASE_URL/api/v3/time" | jq -r '.serverTime')
QS="timestamp=$TS"
SIG=$(printf "%s" "$QS" | openssl dgst -sha256 -hmac "$BINANCE_API_SECRET" | sed 's/^.* //')

curl -s -H "X-MBX-APIKEY: $BINANCE_API_KEY" \
  "$BINANCE_BASE_URL/api/v3/account?$QS&signature=$SIG" | jq
```

## 4) Test order before real order

```bash
SIDE="BUY"
TYPE="LIMIT"
PRICE="30000.00"
QTY="0.001"
TIF="GTC"

TS=$(curl -s "$BINANCE_BASE_URL/api/v3/time" | jq -r '.serverTime')
QS="symbol=BTCUSDT&side=$SIDE&type=$TYPE&timeInForce=$TIF&quantity=$QTY&price=$PRICE&timestamp=$TS"
SIG=$(printf "%s" "$QS" | openssl dgst -sha256 -hmac "$BINANCE_API_SECRET" | sed 's/^.* //')

curl -s -X POST -H "X-MBX-APIKEY: $BINANCE_API_KEY" \
  "$BINANCE_BASE_URL/api/v3/order/test?$QS&signature=$SIG" -d ''
```

## 5) Promote only with explicit confirmation

Replace `/api/v3/order/test` with `/api/v3/order` only after user confirmation for production activity.
