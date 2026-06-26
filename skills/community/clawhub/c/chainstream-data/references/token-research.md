# Token Research Reference

## CLI Commands → REST API Mapping

| CLI Command | REST Endpoint | Method |
|-------------|--------------|--------|
| `token search --keyword X --chain sol` | `GET /v2/token/search?q=X&chains=sol` | GET |
| `token info --chain sol --address ADDR` | `GET /v2/token/sol/ADDR` | GET |
| `token security --chain sol --address ADDR` | `GET /v2/token/sol/ADDR/security` | GET |
| `token holders --chain sol --address ADDR` | `GET /v2/token/sol/ADDR/topHolders` | GET |
| `token candles --chain sol --address ADDR --resolution 1h` | `GET /v2/token/sol/ADDR/candles?resolution=1h` | GET |
| `token pools --chain sol --address ADDR` | `GET /v2/token/sol/ADDR/pools` | GET |

## All Token Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v2/token/search` | Search by keyword (name/symbol/address). Params: `q`, `chains[]`, `limit` |
| GET | `/v2/token/{chain}/{tokenAddress}` | Full token detail |
| GET | `/v2/token/{chain}/{tokenAddress}/metadata` | Name, symbol, decimals, image |
| GET | `/v2/token/{chain}/{tokenAddress}/marketData` | Price, volume, market cap, changes |
| GET | `/v2/token/{chain}/{tokenAddress}/stats` | Buys, sells, volume by time window |
| GET | `/v2/token/{chain}/{tokenAddress}/price` | Current price. `?timestamp=` for historical |
| GET | `/v2/token/{chain}/{tokenAddress}/candles` | OHLCV. Params: `resolution`, `from`, `to`, `limit` |
| GET | `/v2/token/{chain}/{tokenAddress}/holders` | Holder list with balance and percentage |
| GET | `/v2/token/{chain}/{tokenAddress}/topHolders` | Top N holders |
| GET | `/v2/token/{chain}/{tokenAddress}/pools` | Liquidity pools containing this token |
| GET | `/v2/token/{chain}/{tokenAddress}/security` | Honeypot, mint auth, freeze auth, concentration |
| GET | `/v2/token/{chain}/{tokenAddress}/creation` | Deployer, timestamp, initial supply |
| GET | `/v2/token/{chain}/{tokenAddress}/transfers` | Transfer history |
| GET | `/v2/token/{chain}/{tokenAddress}/traders/{tag}` | Traders by tag: smart_money, whale, sniper |
| GET | `/v2/token/{chain}/multi?addresses=A,B` | Batch get tokens (max 50) |
| GET | `/v2/token/{chain}/dev/{devAddress}/tokens` | Tokens created by developer |

## Security Fields

The `/security` endpoint returns critical risk signals:

| Field | Meaning | Risk if True |
|-------|---------|-------------|
| `isHoneypot` | Cannot sell after buying | Critical |
| `hasMintAuthority` | Creator can mint more tokens | High |
| `hasFreezeAuthority` | Creator can freeze transfers | High |
| `topHolderConcentration` | % held by top 10 holders | > 50% is concerning |
| `isOpenSource` | Contract source verified | False is suspicious |

## Response Format

Use `?response_format=concise` (default) for AI agents. `detailed` returns 4-10x more data and should only be used when explicitly needed.

## K-line Resolutions

`1m`, `5m`, `15m`, `1h`, `4h`, `1d`

Timestamps are Unix milliseconds. CLI accepts Unix seconds and converts automatically.
