# Binance WebSocket Operations

Use Spot streams for push market/user events and WS API for request-response over WebSocket.

## Stream endpoints

- Raw streams: `wss://stream.binance.com:9443/ws/<streamName>`
- Combined streams: `wss://stream.binance.com:9443/stream?streams=<s1>/<s2>`
- Market-data-only endpoint: `wss://data-stream.binance.vision`

A single connection is valid for 24 hours. Rotate before hard disconnect.

## Control-plane limits

- Server sends ping frames every 20 seconds.
- Return pong frame quickly with same payload.
- Incoming message cap is 5 messages per second per connection.
- Max 1024 streams per connection.

## Subscribe and inspect combined stream

```bash
wscat -c "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/btcusdt@depth"
```

## WS API endpoint

- Production: `wss://ws-api.binance.com:443/ws-api/v3`
- Testnet: `wss://ws-api.testnet.binance.vision/ws-api/v3`

WS API responses include `rateLimits` by default; keep them enabled while tuning throttling.

## User-data handling

Use user-data stream events (`executionReport`, balance/account updates) as the source of truth for final order state transitions.
Always reconcile uncertain order placement responses against stream events and REST lookup.

## Reconnect strategy

1. Reconnect with jittered backoff.
2. Re-subscribe required streams.
3. Rebuild local sequence context.
4. Compare with REST snapshots to detect missing updates.
