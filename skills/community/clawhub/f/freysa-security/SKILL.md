---
name: "Freysa Security"
description: "On-chain security intelligence for autonomous agents — token honeypot detection, wallet forensics, pre-trade risk checks, CAPTCHA solving, and market data. 27 x402 pay-per-call endpoints on Base."
version: "1.0.0"
author: "Freysa Security"
tags:
  - security
  - crypto
  - defi
  - trading
  - honeypot
  - forensics
  - captcha
  - x402
  - blockchain
  - risk
categories:
  - "crypto"
  - "security"
  - "data"
env:
  - name: "FREYSA_WALLET_KEY"
    description: "Optional: Private key for x402 wallet. If not set, agent pays manually via its own wallet."
    required: false
---

# Freysa Security

**On-chain security intelligence layer for autonomous AI agents.**

27 x402-enabled endpoints on Base mainnet. Pay per request in USDC — no API keys, no signup, no subscription.

## Capabilities

### Security Analysis ($0.25)
- `/api/honeypot-check` — Token honeypot detection via bytecode analysis. Checks buy/sell taxes, hidden mint functions, pause mechanisms, blacklists.
- `/api/address-risk` — Wallet address risk scoring (0-100). Flags scam, phishing, and high-risk addresses.
- `/api/approval-risk` — Scan wallet for dangerous token approvals and unlimited spend allowances.
- `/api/wallet-forensics` — Deep wallet forensic analysis. Traces history, flags suspicious patterns.
- `/api/token-analyze` — Deep token contract analysis including bytecode, ownership, liquidity.

### Pre-Trade Safety ($1.00-$2.50)
- `/api/pre-trade-check` — Comprehensive pre-trade analysis: token + contract + wallet in one call.
- `/api/agent-preflight` — Full agent transaction risk assessment. PROCEED/CAUTION/ABORT verdict.

### CAPTCHA Solving ($0.01)
- `/api/captcha-solve` — Solve CAPTCHA challenges. The #1 most-demanded agent service. Supports text, image, and reCAPTCHA via CapSolver AI backend.

### Smart Contract Review ($0.25)
- `/api/code-review` — Solidity smart contract security review. Flags vulnerabilities, reentrancy, logic bugs.

### Data Feeds ($0.001-$0.05)
- `/api/eth-gas` — **FREE.** Current gas prices on Base.
- `/api/trending` — Trending tokens from DexScreener.
- `/api/base-stats` — Base L2 network statistics.
- `/api/market-overview` — Aggregated crypto market data.
- `/api/crypto-price` — Real-time price for any ticker.
- `/api/fetch` — Web scraping: fetch any URL as structured markdown.

### AI Intelligence ($0.25-$1.00)
- `/api/reason` — Deep reasoning and decision analysis for complex problems.
- `/api/research` — Full research report with web research and source citations.
- `/api/synthesize` — AI data synthesis from multiple sources.

## How to Use

### From any agent (manual x402 payment):

```bash
# 1. Call endpoint → get 402
curl -X POST https://economic-agent-369.freysa.dev/api/honeypot-check \
  -H "Content-Type: application/json" \
  -d '{"token_address":"0x..."}'

# 2. Response includes PAYMENT-REQUIRED header with payment details
# 3. Sign EIP-3009 authorization with your wallet
# 4. Retry with PAYMENT-SIGNATURE header
curl -X POST https://economic-agent-369.freysa.dev/api/honeypot-check \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64-encoded-payment>" \
  -d '{"token_address":"0x..."}'
```

### With x402 SDK (Python):

```python
from x402 import x402_requests
response = x402_requests.post(
    "https://economic-agent-369.freysa.dev/api/honeypot-check",
    json={"token_address": "0x..."},
    wallet=my_wallet
)
```

## Pricing

| Tier | Price | Examples |
|------|-------|---------|
| Free | $0.00 | gas prices |
| Data | $0.001 | trending, prices, stats, web scraping |
| Utility | $0.01 | CAPTCHA solving |
| Security | $0.25 | honeypot, address risk, forensics, code review |
| Premium | $1.00-$2.50 | pre-trade check, agent preflight |

## Network

**Chain:** Base (eip155:8453)
**Settlement:** USDC via x402 protocol
**Facilitator:** Coinbase CDP (api.cdp.coinbase.com/platform/v2/x402)
**PayTo:** `0x6D8abB282C35D45E3C773aD8a67b288Ac35fd1e9`

## Discovery

- **x402 manifest:** https://economic-agent-369.freysa.dev/.well-known/x402
- **Agent Card:** https://economic-agent-369.freysa.dev/.well-known/agent-card.json
- **OpenAPI:** https://economic-agent-369.freysa.dev/openapi.json
- **API Base:** https://economic-agent-369.freysa.dev

## Example Workflow

### Trading Agent Pre-Flight

```
1. Agent finds new token on DexScreener
2. → Calls honeypot-check ($0.25) → "SAFE"
3. → Calls address-risk on deployer ($0.25) → "LOW RISK"
4. → Calls pre-trade-check ($1.00) → "GO"
5. → Executes trade
Total: $1.50 for $500+ risk protection
```

## Support

Email: admin@economic-agent-369.freysa.dev