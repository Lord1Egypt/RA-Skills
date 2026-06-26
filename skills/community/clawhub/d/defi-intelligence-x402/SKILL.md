---
name: defi-intelligence-x402
description: 16-tool DeFi intelligence agent — token prices, swap quotes, wallet analytics, portfolio tracking, DeFi positions, gas oracle, ENS resolution, and contract reads via x402.
version: 1.0.0
homepage: https://github.com/plagtech/defi-intelligence-skill
metadata:
  openclaw:
    primaryEnv: RESEARCH_API_KEY
    envVars:
      - name: RESEARCH_API_KEY
        required: true
        description: API key or x402 subscription key for the gateway.
      - name: RESEARCH_GATEWAY_URL
        required: false
        description: Gateway URL. Defaults to https://gateway.spraay.app
    requires:
      bins:
        - curl
        - python3
---

# DeFi Intelligence

16 endpoints for on-chain analytics, token prices, swap quotes, portfolio tracking, DeFi positions, wallet profiling, and smart contract reads. Each call is a real x402 micropayment ($0.001–$0.015 USDC).

## How to call endpoints

```bash
bash {baseDir}/scripts/defi.sh METHOD ENDPOINT '{"key":"value"}'
```

GET endpoints pass JSON as query params. POST endpoints send JSON body.

## Workflow strategies

**Token research** — get prices, check swap quotes across DEXes, look up the contract via contract/read, resolve any ENS names involved.

**Wallet profiling** — resolve ENS to address, pull balances, get wallet analytics (activity tier, risk signals), check portfolio tokens and NFTs, review DeFi positions, pull tx history.

**Yield analysis** — check DeFi positions for an address, get token prices to calculate USD values, compare swap rates for entry/exit.

**Market monitoring** — use oracle/prices for aggregated feeds, oracle/gas for chain congestion, oracle/fx for stablecoin depegs, prices for quick multi-token lookups.

**Due diligence** — combine wallet analytics (risk signals) with tx history, portfolio composition, and DeFi position exposure for a complete profile.

Always include token symbols, USD values, and chain context in your responses. Format large numbers with commas.

## Available endpoints (16 tools)

### Price & Oracle Data

**Oracle Prices** — $0.008
Aggregated oracle price feed across multiple sources.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/oracle/prices '{"symbols":"ETH,BTC,SOL"}'
```

**Token Prices** — $0.002
Multi-token price feed across major assets. Cached, low-latency.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/prices '{"symbols":"ETH,BTC,USDC"}'
```

**Gas Prices** — $0.005
Real-time gas prices for Base and other supported EVM chains.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/oracle/gas '{"chain":"base"}'
```

**Stablecoin FX** — $0.008
Stablecoin FX rates: USDC, USDT, DAI, EURC, pyUSD, and more.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/oracle/fx '{}'
```

### Swap Intelligence

**Swap Quote** — $0.008
Get a swap quote across Uniswap V3, Aerodrome, and other DEXes on Base.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/swap/quote '{"tokenIn":"USDC","tokenOut":"ETH","amount":"1000"}'
```

**Swap Tokens** — $0.001
List supported swap tokens with addresses, decimals, and metadata.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/swap/tokens '{}'
```

### Wallet Analytics

**Wallet Profile** — $0.01
Wallet profile: balances, top tokens, activity tier, age, risk signals.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/analytics/wallet '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**Transaction History** — $0.008
Transaction history for any address across supported chains.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/analytics/txhistory '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**Balances** — $0.005
Multi-chain balance lookup for any address.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/balances '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

### Portfolio & DeFi

**Portfolio Tokens** — $0.005
Full token portfolio for an address across supported chains.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/portfolio/tokens '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**Portfolio NFTs** — $0.005
NFT holdings for an address across supported chains.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/portfolio/nfts '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**DeFi Positions** — $0.008
Open DeFi positions across supported protocols — lending, staking, LP, vaults.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/defi/positions '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

### Identity & Contracts

**ENS Resolution** — $0.002
Resolve an ENS name, Basename, or address to its canonical identity.
```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/resolve '{"name":"vitalik.eth"}'
```

**Read Contract** — $0.002
Read from any smart contract via a view/pure function call.
```bash
bash {baseDir}/scripts/defi.sh POST /api/v1/contract/read '{"address":"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","function":"totalSupply","chain":"base"}'
```

### Execution

**Execute Swap** — $0.015
Execute a token swap on Base via the MangoSwap router. Use swap/quote first to preview.
```bash
bash {baseDir}/scripts/defi.sh POST /api/v1/swap/execute '{"tokenIn":"USDC","tokenOut":"ETH","amount":"100","slippage":0.5}'
```

**Write Contract** — $0.01
Submit a state-changing smart contract transaction. Use with caution.
```bash
bash {baseDir}/scripts/defi.sh POST /api/v1/contract/write '{"address":"0x...","function":"approve","args":["0x...",1000000],"chain":"base"}'
```

## Cost reference

| Endpoint | Cost | Type |
|----------|------|------|
| Swap Tokens | $0.001 | Read |
| Token Prices | $0.002 | Read |
| ENS Resolve | $0.002 | Read |
| Contract Read | $0.002 | Read |
| Gas Prices | $0.005 | Read |
| Balances | $0.005 | Read |
| Portfolio Tokens | $0.005 | Read |
| Portfolio NFTs | $0.005 | Read |
| Oracle Prices | $0.008 | Read |
| Stablecoin FX | $0.008 | Read |
| Swap Quote | $0.008 | Read |
| Tx History | $0.008 | Read |
| DeFi Positions | $0.008 | Read |
| Wallet Profile | $0.01 | Read |
| Contract Write | $0.01 | Write |
| Execute Swap | $0.015 | Write |

Data sourced from Alchemy, CoinGecko, Uniswap V3, Aerodrome, and on-chain indexers.
