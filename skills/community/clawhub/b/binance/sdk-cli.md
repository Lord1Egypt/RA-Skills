# Binance SDK and CLI Workflows

Binance provides official SDK connectors for major languages.
There is no single official Binance terminal CLI that covers all Spot workflows.
Use `curl` for deterministic operations and official connectors for larger integrations.

## Official connectors

- Python: `binance-sdk-spot`
- Node.js: `@binance/spot`
- Go: `github.com/binance/binance-connector-go`
- Dotnet: `Binance.Spot`

## Install examples

```bash
pip install binance-sdk-spot
npm install @binance/spot
go get github.com/binance/binance-connector-go
dotnet add package Binance.Spot
```

## Python quick call

```python
from binance_sdk_spot.spot import Spot

client = Spot(api_key="...", private_key="...")
print(client.ticker_price(symbol="BTCUSDT"))
```

## Node.js quick call

```js
import { Spot } from '@binance/spot';

const client = new Spot({
  apiKey: process.env.BINANCE_API_KEY,
  privateKey: 'YOUR_PRIVATE_KEY',
});

const price = await client.tickerPrice({ symbol: 'BTCUSDT' });
console.log(price);
```

## Terminal helper strategy

When the user asks for CLI-only operation:
- keep a shell function for signing requests
- use `curl + jq` for all critical paths
- log payload and response summaries in `~/binance/runbooks.md`

For signature edge cases, use Binance official signature examples repository.
