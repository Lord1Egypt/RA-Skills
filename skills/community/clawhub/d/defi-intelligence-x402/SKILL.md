---
name: defi-intelligence-x402
description: "DeFi analytics and on-chain execution via Spraay x402 — token prices, swap quotes, wallet profiling, portfolio/NFTs, DeFi positions, gas oracle, ENS, contract reads. Plus swap execution and contract writes. USDC micropayments on Base/Solana. Write ops are irreversible."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - curl
---

# DeFi Intelligence

16 endpoints for on-chain analytics, token prices, swap quotes, portfolio tracking, DeFi positions, wallet profiling, and smart contract reads — plus swap execution and contract writes. Each call is a real x402 micropayment ($0.001–$0.015 USDC) settled on Base or Solana mainnet.

## ⚠️ Before you install

> **This skill sends data to an external paid gateway** (`gateway.spraay.app`) and can execute **irreversible on-chain transactions**.
>
> - **Network access:** Every endpoint call transmits your request (including wallet addresses, token symbols, and contract call data) to the Spraay x402 gateway over HTTPS. Data leaves your local environment.
> - **Real money:** Each call costs USDC via the x402 payment protocol. Your agent's wallet is debited for every paid request.
> - **Write operations:** The `swap/execute` and `contract/write` endpoints submit **irreversible blockchain transactions** that can spend tokens, grant approvals, or change on-chain state. These cannot be undone.
> - **Privacy:** Wallet addresses, balances, transaction history, portfolio holdings, NFT data, and DeFi positions are sent to the gateway. The gateway operator may log or retain this data.
>
> **Install only if you trust the gateway operator and are comfortable sending wallet-related data to this service.** Use a dedicated wallet with limited funds for testing. Require explicit human approval before any write operation.

## How to call endpoints

```bash
bash {baseDir}/scripts/defi.sh METHOD ENDPOINT '{"key":"value"}'
```

The script requires `bash` and `curl`. GET endpoints pass JSON as query params. POST endpoints send JSON body. All calls go to `https://gateway.spraay.app`.

## Workflow strategies

**Token research** — get prices, check swap quotes across DEXes, look up the contract via contract/read, resolve any ENS names involved.

**Wallet profiling** — resolve ENS to address, pull balances, get wallet analytics (activity tier, risk signals), check portfolio tokens and NFTs, review DeFi positions, pull tx history.

**Yield analysis** — check DeFi positions for an address, get token prices to calculate USD values, compare swap rates for entry/exit.

**Market monitoring** — use oracle/prices for aggregated feeds, oracle/gas for chain congestion, oracle/fx for stablecoin depegs, prices for quick multi-token lookups.

**Due diligence** — combine wallet analytics (risk signals) with tx history, portfolio composition, and DeFi position exposure for a complete profile.

Always include token symbols, USD values, and chain context in your responses. Format large numbers with commas.

## Available endpoints (16 tools)

### Price & Oracle Data (read-only)

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

### Swap Intelligence (read-only)

**Swap Quote** — $0.008
Get a swap quote across Uniswap V3, Aerodrome, and other DEXes on Base. This is a read-only price check — no tokens are moved.

```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/swap/quote '{"tokenIn":"USDC","tokenOut":"ETH","amount":"1000"}'
```

**Swap Tokens** — $0.001
List supported swap tokens with addresses, decimals, and metadata.

```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/swap/tokens '{}'
```

### Wallet Analytics (read-only, sends address to gateway)

> **Privacy note:** These endpoints transmit blockchain addresses and return financial data about those addresses. The gateway operator receives and may log the queried addresses.

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

### Portfolio & DeFi (read-only, sends address to gateway)

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

**ENS Resolution** — $0.002 (read-only)
Resolve an ENS name, Basename, or address to its canonical identity.

```bash
bash {baseDir}/scripts/defi.sh GET /api/v1/resolve '{"name":"vitalik.eth"}'
```

**Read Contract** — $0.002 (read-only)
Read from any smart contract via a view/pure function call.

```bash
bash {baseDir}/scripts/defi.sh POST /api/v1/contract/read '{"address":"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","function":"totalSupply","chain":"base"}'
```

### ⚠️ Execution (WRITE — requires human approval)

> **These endpoints submit irreversible blockchain transactions.** The agent MUST request explicit human confirmation before calling either endpoint. Show the user the full parameters (token, amount, recipient, chain, slippage) and wait for approval. Never auto-execute.

**Execute Swap** — $0.015 ⚠️ WRITE
Execute a token swap on Base via the MangoSwap router. **Use swap/quote first** to preview the trade. Tokens will leave the wallet.

```bash
# ALWAYS get human approval before running this
bash {baseDir}/scripts/defi.sh POST /api/v1/swap/execute '{"tokenIn":"USDC","tokenOut":"ETH","amount":"100","slippage":0.5}'
```

**Write Contract** — $0.01 ⚠️ WRITE
Submit a state-changing smart contract transaction. **Use with extreme caution.** Can grant token approvals, transfer assets, or change contract state. Irreversible.

```bash
# ALWAYS get human approval before running this
bash {baseDir}/scripts/defi.sh POST /api/v1/contract/write '{"address":"0x...","function":"approve","args":["0x...",1000000],"chain":"base"}'
```

## Cost reference

| Endpoint         | Cost   | Type       |
| ---------------- | ------ | ---------- |
| Swap Tokens      | $0.001 | Read       |
| Token Prices     | $0.002 | Read       |
| ENS Resolve      | $0.002 | Read       |
| Contract Read    | $0.002 | Read       |
| Gas Prices       | $0.005 | Read       |
| Balances         | $0.005 | Read       |
| Portfolio Tokens | $0.005 | Read       |
| Portfolio NFTs   | $0.005 | Read       |
| Oracle Prices    | $0.008 | Read       |
| Stablecoin FX    | $0.008 | Read       |
| Swap Quote       | $0.008 | Read       |
| Tx History       | $0.008 | Read       |
| DeFi Positions   | $0.008 | Read       |
| Wallet Profile   | $0.01  | Read       |
| Contract Write   | $0.01  | ⚠️ Write  |
| Execute Swap     | $0.015 | ⚠️ Write  |

Data sourced from Alchemy, CoinGecko, Uniswap V3, Aerodrome, and on-chain indexers.

## Changelog

### v1.1.0

- **Added YAML frontmatter permissions** — declared `bins: [bash, curl]` under `metadata.openclaw.requires`. Fixes "MCP Least Privilege" audit finding.
- **Fixed description-behavior mismatch** — description now explicitly states the skill includes swap execution and contract writes, not just read-only analytics. Fixes 2 HIGH severity findings.
- **Removed off-scope endpoints** — web search, paper search, and generic research endpoints moved to AI Content Creator where they belong. Fixes "Intent-Code Divergence" and "Context-Inappropriate Capability" findings.
- **Added real-money and privacy warnings** — prominent disclosure about external data transmission, wallet data privacy, irreversible write operations, and USDC cost per call. Fixes 3 "Missing User Warnings" findings.
- **Added human approval requirement** — swap/execute and contract/write now require explicit user confirmation before calling. Addresses destructive/irreversible action warning.
- **Updated description** — accurate, keyword-rich, within 300-char limit.

### v1.0.0

- Initial release with 16 DeFi endpoints.

## Related terms

DeFi analytics, token prices, swap quotes, DEX aggregator, wallet profiling,
portfolio tracker, NFT holdings, DeFi positions, gas oracle, ENS resolution,
contract read, contract write, swap execution, on-chain intelligence,
x402 payments, USDC micropayments, Base chain, Solana, agent DeFi tools
