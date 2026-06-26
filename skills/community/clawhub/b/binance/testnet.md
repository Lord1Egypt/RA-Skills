# Binance Spot Testnet

Use Spot testnet for validating auth, filters, and order payloads before production.

## Endpoints

```text
REST: https://testnet.binance.vision
WS Streams: wss://stream.testnet.binance.vision/ws
WS API: wss://ws-api.testnet.binance.vision/ws-api/v3
```

Spot testnet supports only `/api` routes. SAPI and margin routes are unavailable.

## API keys

- Generate testnet keys from Spot testnet tooling.
- Key and secret are shown only once; store immediately.
- API keys persist through monthly testnet data resets.

## Expected resets

Spot testnet generally resets approximately monthly.
Order books, trades, balances, and orders can be cleared on reset.

## Safe validation sequence

1. Validate connectivity with `ping` and `time`.
2. Check symbol filters via `exchangeInfo`.
3. Verify signed account call.
4. Execute `order/test` for each new payload shape.
5. Validate user-data events in WS stream or WS API.

## Promotion checklist

Promote to production only after:
- testnet order/test payloads pass
- filter validation is automated
- error handling for `-1021`, `-1022`, and `-1007` is proven
- user explicitly confirms production execution
