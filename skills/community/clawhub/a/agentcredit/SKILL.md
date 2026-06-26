# AgentCredit — Flash Microloans for AI Agents

## Description

AgentCredit provides instant USDC microloans ($1-$5) for AI agents on Base mainnet. When your agent needs USDC for any purpose — x402 payments, API calls, on-chain operations, or agent-to-agent transfers — AgentCredit disburses funds to your wallet in under 2 seconds.

## Security & Trust

### Credentials & Signing

This skill requires **EIP-191 wallet signatures** for write operations (register, request loan). Your agent must have access to wallet signing capabilities.

**Key points:**
- This skill does NOT store or request private keys
- Direct loan requests (REST API / MCP) require an EIP-191 signature
- In facilitator mode, credit is extended transparently during x402 settlement — no additional signature needed (the x402 payment itself is cryptographic proof)
- Read operations (check_credit, list loans) require NO signatures

### On-Chain Addresses

- **Pool wallet**: `0x510a64F194CB6196d34C93717d88f13aCF0C979f` ([BaseScan](https://basescan.org/address/0x510a64F194CB6196d34C93717d88f13aCF0C979f))
- **USDC contract**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` ([BaseScan](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913))
- **Network**: Base mainnet (CAIP-2: eip155:8453)

### How Facilitator Mode Works

AgentCredit operates as an x402 facilitator. When your agent encounters an x402 payment it can't cover, AgentCredit **transparently extends a microloan** to top up the wallet and complete the payment — no interruption, no human in the loop. The agent repays from subsequent revenue.

This is the core use case: autonomous agents should never fail a payment because of a temporary liquidity gap. Built-in safeguards prevent abuse:
- Max $5 per loan, max $10 total exposure, max 3 outstanding loans
- Agents must register (one-time, with EIP-191 signature) before credit is available
- First 100 x402 settlements are free with no registration
- Overdue loans block further facilitator settlements until repaid

### Limits & Caps

| Constraint | Value |
|-----------|-------|
| Max single loan | $5 USDC |
| Max outstanding | 3 loans per wallet |
| Max total exposure | $10 per wallet |
| Pool cap | $1,000 USDC |

### Source & Links

- **Source**: [github.com/spekn-ai/agentcredit](https://github.com/spekn-ai/agentcredit)
- **API**: https://agentlending.spekn.com
- **Operator**: [Spekn](https://spekn.com)
- **Status**: MVP / experimental — use test amounts only

## Capabilities

- **Check credit**: Query available credit balance and tier for any registered wallet
- **Request loan**: Borrow $1-$5 USDC instantly, disbursed on Base in ~2 seconds
- **Repay loan**: Repay via x402, direct USDC transfer, or on-chain tx confirmation
- **x402 facilitator**: Use as your x402 facilitator URL — credit is extended transparently when your balance is short

## Integration

### As x402 Facilitator (recommended — fully autonomous)
```typescript
import { wrapFetch } from '@x402/fetch';
const fetchWith402 = wrapFetch(fetch, walletClient, {
  facilitatorUrl: 'https://agentlending.spekn.com',
});
```
First 100 settlements free. Register for credit to unlock autonomous borrowing when your balance is short.

### As MCP Server
```json
{
  "mcpServers": {
    "agentcredit": {
      "type": "streamable-http",
      "url": "https://agentlending.spekn.com/mcp"
    }
  }
}
```

Tools: `check_credit`, `request_loan`, `repay_loan`

### As REST API
```
POST /agents/register        — Register wallet (EIP-191 signature required)
GET  /agents/:wallet/credit  — Check credit (no auth)
GET  /agents/:wallet/loans   — List loans (no auth)
POST /loans/request          — Request loan (EIP-191 signature required)
GET  /loans/:id/pay          — Repay via x402 (returns 402)
```

Full docs: https://agentlending.spekn.com/llms-full.txt

## Fee Model

Loans are designed for **fast repayment** — borrow, use, repay within hours. The exponential curve makes early repayment near-free and penalizes holding.

| Timing | $1 loan cost (BB tier) | Effective rate |
|--------|----------------------|----------------|
| 1 hour | ~$1.005 | 0.5% |
| 4 hours (target term) | ~$1.006 | 0.6% |
| 24 hours | ~$1.02 | 2% |
| 7 days (penalty zone) | ~$2.50 | 150% |

- **Origination fee**: $0.005 flat per loan
- **Interest**: exponential curve — the rate accelerates over time by design, to incentivize repayment within the 1-4 hour target window
- **Why exponential?** Flat rates would make it rational to hold loans indefinitely. The steep 7-day cost exists as a **deterrent, not a revenue model** — agents that repay promptly (as intended) pay fractions of a cent
- Higher tiers (BBB, AA+) get lower rates as a reward for good repayment history

## Authentication

Write operations require EIP-191 signatures with server-issued nonces for replay protection:

1. **Get a nonce**: `GET /auth/nonce?wallet=<addr>&action=register|request_loan` — returns a single-use nonce valid for 5 minutes
2. **Sign the message** (include the nonce):
   - Register: sign `AgentCredit:register:<wallet_lowercase>:<nonce>`
   - Request loan: sign `AgentCredit:request_loan:<wallet_lowercase>:<amountUsdc>:<nonce>`
3. **Send request** with `signature` and `nonce` in the body

Read operations and repayments do not require signatures.

## Discovery

- x402: https://agentlending.spekn.com/.well-known/x402.json
- A2A Agent Card: https://agentlending.spekn.com/.well-known/agent-card.json
- MCP: https://agentlending.spekn.com/mcp
- llms.txt: https://agentlending.spekn.com/llms.txt
