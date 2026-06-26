# Logo Proxy

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Proxy TradingView Logo by URL

`GET /logo`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/logo?url=apple.svg&big=true' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY' \
	--output apple.svg
```

## Proxy TradingView Logo by Path

`GET /logo/{path}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/logo/apple.svg' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY' \
	--output apple.svg
```
