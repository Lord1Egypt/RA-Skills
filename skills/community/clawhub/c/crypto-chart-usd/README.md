# Crypto charting with USD pricing (1s)

Real-time multi-token, multi-chain crypto chart feed with 1-second OHLC ticks and USD pricing from the Bitquery Trading.Tokens API. Supports **Arbitrum**, **Base**, **Matic**, **Ethereum**, **Solana**, **Binance Smart Chain**, **Tron**, and **Optimism** — all tokens on these chains.

## Required

- **BITQUERY_API_KEY** — Set in your environment. The token is only supported in the WebSocket URL (`?token=...`); do not print or log the full URL. See SKILL.md for security notes.
- Python 3 and `pip install 'gql[websockets]'`

## Run the stream

```bash
python scripts/stream_crypto_chart.py
# or with timeout: python scripts/stream_crypto_chart.py --timeout 60
```

## Docs

See **SKILL.md** for full instructions, subscription shape, and output format.
