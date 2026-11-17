# Exchange API notes

- **Coinbase**: `api.exchange.coinbase.com/products/{SYM}-USD/ticker` — public, no key.
- **Kraken**: `api.kraken.com/0/public/Ticker?pair={PAIR}` — BTC uses `XBTUSD`, not `BTCUSD`.
- **Bitstamp**: `www.bitstamp.net/api/v2/ticker/{sym}usd/` — lowercase symbol, no dash.
- **Gemini**: `api.gemini.com/v1/pubticker/{sym}usd` — lowercase symbol, no dash.
- **OKX**: `www.okx.com/api/v5/market/ticker?instId={SYM}-USDT` — quoted in USDT, not USD (close enough for spread purposes, but introduces minor USDT-peg noise).
- **Binance**: excluded — public REST returns HTTP 451 "Service unavailable from a restricted location" from many cloud/hosted IP ranges.

All requests are unauthenticated GETs with a short timeout (10s) and fail
soft — if an exchange doesn't respond or doesn't list the symbol, it's
dropped from that symbol's comparison rather than crashing the run.
