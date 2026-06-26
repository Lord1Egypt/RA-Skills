---
name: chartsplat-x402
description: Generate beautiful charts by paying per request with x402 micropayments (USDC on Base) instead of an API key. Use when the user wants a chart and has no CHARTSPLAT_API_KEY but has an EVM wallet, or mentions x402, USDC, micropayment, or pay-per-call. Costs ~$0.005 per chart. Returns PNG images. Supports line, bar, pie, doughnut, radar, polar area, candlestick, and OHLC charts.
version: 1.0.1
license: MIT
compatibility: Requires Node.js 20+ and an EVM wallet with a small USDC balance on Base mainnet (eip155:8453). No CHARTSPLAT_API_KEY needed.
metadata:
  author: workingdevshero
  version: "1.0.1"
  homepage: https://chartsplat.com
  openclaw:
    requires:
      env:
        - X402_PRIVATE_KEY
      bins:
        - node
        - npx
    primaryEnv: X402_PRIVATE_KEY
    emoji: "coin"
    homepage: https://chartsplat.com
    os:
      - darwin
      - linux
      - win32
    install:
      - kind: node
        package: chartsplat-x402-cli
        bins: [chartsplat-x402]
        label: "Install Chart Splat (x402) CLI via npm"
---

# Chart Splat (x402)

Generate beautiful charts by paying per request with [x402](https://x402.org) micropayments — no signup, no API key, no subscription. The agent's wallet pays ~$0.005 USDC on Base mainnet for each chart.

This is the wallet-based counterpart to the standard `chart-splat` skill (which authenticates with an API key). Use whichever fits the user's setup.

## Prerequisites

- An EVM wallet with **≥ $0.05 USDC on Base mainnet** (`eip155:8453`)
- Private key exported as `X402_PRIVATE_KEY` (a hex string starting with `0x`)
- Node.js 20+

The buyer never submits an on-chain transaction directly. The Coinbase x402 facilitator handles settlement and pays gas. See [references/x402-protocol.md](references/x402-protocol.md) for protocol detail.

## Supported Chart Types

| Type | Best For |
|------|----------|
| `line` | Trends over time |
| `bar` | Comparing categories |
| `pie` | Parts of a whole |
| `doughnut` | Parts of a whole (with center space) |
| `radar` | Multivariate comparison |
| `polarArea` | Comparing categories with radial layout |
| `candlestick` | Financial/crypto OHLC price data |
| `ohlc` | Financial/crypto OHLC price data (bar variant) |

## Method 1: CLI (Preferred)

Use the `chartsplat-x402` CLI via npx — no install required.

```bash
npx -y chartsplat-x402-cli bar \
  --labels "Q1,Q2,Q3,Q4" \
  --data "50,75,60,90" \
  --title "Quarterly Revenue" \
  --color "#8b5cf6" \
  -o chart.png
```

The CLI handles the full x402 flow: sends the request, signs the EIP-3009 authorization on the 402 response, retries with the `PAYMENT-SIGNATURE` header, and saves the resulting PNG. On success, it prints a BaseScan URL for the settlement transaction.

### CLI Options

| Flag | Description |
|------|-------------|
| `-l, --labels <csv>` | Comma-separated labels |
| `-d, --data <csv>` | Comma-separated numeric values |
| `-t, --title <text>` | Chart title |
| `--label <text>` | Dataset label for legend |
| `-c, --color <hex>` | Background color |
| `-w, --width <px>` | Image width (default: 800) |
| `--height <px>` | Image height (default: 600) |
| `-o, --output <file>` | Output file path (default: chart.png) |
| `--config <file>` | JSON config file for complex charts |
| `--private-key <key>` | Wallet key (or set `X402_PRIVATE_KEY`) |

### CLI Chart Commands

```bash
npx -y chartsplat-x402-cli line       -l "Mon,Tue,Wed,Thu,Fri" -d "100,200,150,300,250" -o line.png
npx -y chartsplat-x402-cli bar        -l "A,B,C"       -d "10,20,30"  -o bar.png
npx -y chartsplat-x402-cli pie        -l "Red,Blue,Green" -d "30,50,20" -o pie.png
npx -y chartsplat-x402-cli doughnut   -l "Yes,No,Maybe" -d "60,25,15" -o doughnut.png
npx -y chartsplat-x402-cli radar      -l "Speed,Power,Range,Durability,Precision" -d "80,90,70,85,95" -o radar.png
npx -y chartsplat-x402-cli polararea  -l "N,E,S,W"     -d "40,30,50,20" -o polar.png
npx -y chartsplat-x402-cli candlestick --config ohlc.json -o chart.png
```

### Candlestick Charts

Candlestick and OHLC charts require a JSON config file since the data format is more complex than a simple CSV list. Use `--config` to provide a file with OHLC data points.

```bash
npx -y chartsplat-x402-cli candlestick --config ohlc.json -o candlestick.png
```

Config format (`ohlc.json`):

```json
{
  "type": "candlestick",
  "data": {
    "datasets": [{
      "label": "VVV Price",
      "data": [
        { "x": 1740441600000, "o": 4.23, "h": 4.80, "l": 4.10, "c": 4.45 },
        { "x": 1740528000000, "o": 4.45, "h": 5.50, "l": 4.30, "c": 5.34 },
        { "x": 1740614400000, "o": 5.34, "h": 6.20, "l": 5.10, "c": 5.97 }
      ]
    }]
  }
}
```

Each OHLC data point requires: `x` (numeric timestamp in ms, or a date string like `"2025-02-25"`), `o` (open), `h` (high), `l` (low), `c` (close).

### Complex Charts via Config File

For multi-dataset or customized charts, write a JSON config file then pass it to the CLI:

```bash
npx -y chartsplat-x402-cli bar --config chart-config.json -o chart.png
```

See [examples/sample-charts.json](examples/sample-charts.json) for ready-to-use config samples and [chartsplat.com/docs](https://chartsplat.com/docs) for the full schema.

## Method 2: Programmatic (`@x402/fetch`)

For embedding directly in TypeScript/JavaScript:

```js
const { wrapFetchWithPayment, x402Client } = require('@x402/fetch');
const { registerExactEvmScheme } = require('@x402/evm/exact/client');
const { privateKeyToAccount } = require('viem/accounts');

const account = privateKeyToAccount(process.env.X402_PRIVATE_KEY);
const client = new x402Client();
registerExactEvmScheme(client, { signer: account });
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

const res = await fetchWithPayment('https://api.chartsplat.com/chart', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'bar',
    data: { labels: ['A', 'B'], datasets: [{ data: [1, 2] }] },
  }),
});
const { image } = await res.json();
```

Use the **v2 `@x402/*` packages** — the legacy unscoped `x402-fetch@1.x` will not work with the chart-splat server. See [references/x402-protocol.md](references/x402-protocol.md).

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `X402_PRIVATE_KEY` | _(required)_ | Hex private key for the paying wallet |
| `CHARTSPLAT_API_URL` | `https://api.chartsplat.com` | API base URL — override to point at a testnet server |

## Testnet (Base Sepolia)

Pointing at a Base Sepolia chart-splat server:

```bash
export CHARTSPLAT_API_URL=https://your-sepolia-server.example.com
npx -y chartsplat-x402-cli bar -l "A,B,C" -d "1,2,3" -o chart.png
```

Get test USDC from the [Circle faucet](https://faucet.circle.com) (select **Base Sepolia**).

## Output Handling

- Charts are saved as PNG files at the specified output path (default: `chart.png`)
- For messaging platforms (Discord, Slack), return the file path: `MEDIA: /path/to/chart.png`
- The CLI prints a settlement transaction URL on success for buyer auditing

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `wallet private key required` | Missing wallet | Export `X402_PRIVATE_KEY` or pass `--private-key` |
| `settlement failed` (second 402) | Wallet has insufficient USDC | Top up; ~$0.01 per chart is enough headroom |
| `402` keeps repeating | Wrong package version (v1 vs v2) | Confirm `chartsplat-x402-cli` is up to date |
| `no scheme matches` | Network mismatch | Server advertises `eip155:8453` — don't override the network on the client |
| Signature rejected after long delay | Validity window (default 1h) expired | Re-run; system clock skew may also cause this |

See [references/x402-protocol.md](references/x402-protocol.md) for protocol gotchas.

## Tips

- The CLI accepts the full Chart Splat request body via `--config` — see [examples/sample-charts.json](examples/sample-charts.json) for ready-to-use samples or [chartsplat.com/docs](https://chartsplat.com/docs) for the full schema
- For pie/doughnut charts, pass an array of colors via `--config` so each segment gets a distinct color
- Default dimensions (800x600) suit most uses; raise via `options.width` / `options.height` for presentations
- Settlement is logged with a BaseScan URL — keep these for accounting
