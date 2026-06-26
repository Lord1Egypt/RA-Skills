# Conto Policy Skill for OpenClaw

## Why Conto?

Your AI agent has a wallet — but wallets only give you flat spending limits. Conto adds the policy layer that's missing: per-transaction caps, daily/weekly/monthly budgets, category restrictions (block gambling, allow only API providers), counterparty blocklists, business hours enforcement, velocity rate limiting, approval workflows for high-value transactions, geographic/OFAC compliance, and x402 API payment controls. 20+ rule types, all evaluated before every payment, with full audit trails in a dashboard.

Conto works with any wallet provider (Sponge, Privy, or your own keys) on any EVM chain or Solana.

## Quick Start

### 1. Sign up and install

Create an account at [conto.finance](https://conto.finance) (or use `http://localhost:3006` for local development).

Then install the skill:

```bash
npx clawhub@latest install kwattana/conto
```

### 2. Find your OpenClaw wallet address

Conto needs your wallet address to track spending. Your address depends on how your OpenClaw agent's wallet is set up:

**If you already have a Sponge wallet** (most OpenClaw setups), ask your agent:

```
What is my wallet address?
```

Or from the CLI:

```bash
openclaw agent --agent main -m "What is my Tempo wallet address?"
```

The agent will call `get_balance` and return your address (e.g., `0x80Ca...`). This is the same address across all EVM chains (Base, Tempo, Ethereum, Polygon).

**If you use a different wallet provider** (not Sponge), find the EVM address from your provider's dashboard or config. For example, if your agent uses a Privy embedded wallet, check your Privy dashboard. If you manage your own keys, use the public address of the private key your agent is configured with.

**If you don't have a wallet yet**, the Sponge MCP server creates one automatically when your agent first checks its balance. Just ask:

```
Show me my wallet balances
```

A new wallet is provisioned and the address is returned. Use this address in the next step.

> **Important:** Use the address your agent actually controls. If your agent uses Sponge MCP tools for transfers (`mcp__sponge__tempo_transfer`, `mcp__sponge__evm_transfer`), register the Sponge wallet address. If you use a different wallet provider, register that address instead. The address registered in Conto must match the wallet that sends the on-chain transactions.

### 3. Set up your agent in Conto

Sign in to the [Conto dashboard](https://conto.finance):

1. **Create an agent**: Agents > Create Agent > name it, set type to CUSTOM, status ACTIVE
2. **Register your wallet**: Wallets > Add Wallet > paste the wallet address from step 2, set custody type to EXTERNAL (since OpenClaw holds the keys via Sponge, not Conto)
3. **Link wallet to agent**: Agents > your agent > Wallets tab > link the wallet, set spend limits ($200/tx, $1000/day)
4. **Generate an SDK key**: Agents > your agent > SDK Keys > Generate New Key
   - Select **Admin** key type (lets the agent create and manage policies)
   - Select **Standard** for payment approval only
   - Copy the key immediately — it's only shown once

### 4. Configure OpenClaw

Add the skill entry to `~/.openclaw/openclaw.json` under the `skills` section:

```json
{
  "skills": {
    "entries": {
      "conto": {
        "env": {
          "CONTO_SDK_KEY": "conto_agent_your_key_here",
          "CONTO_API_URL": "https://conto.finance"
        }
      }
    }
  }
}
```

Replace the key with yours. Use `http://localhost:3006` for local development.

## How to Invoke

### Telegram / Discord / WhatsApp

Your agent is already running in chat. Just type:

```
/conto list my policies
```

Or mention policies/payments naturally — the skill activates automatically:

```
Create a spending policy that limits each transaction to 200 pathUSD
```

### CLI

Pass your message with `--agent` and `-m`:

```bash
openclaw agent --agent main -m "/conto list my policies"
```

The `--agent main` tells OpenClaw which agent to use. The `-m` flag passes your message. `/conto` explicitly triggers the skill, but you can also just describe what you want and OpenClaw will match it.

## Create Policies

With an admin SDK key, you can set policies directly from the agent.

### Set a per-transaction limit

```
/conto create a policy that limits each transaction to 200 pathUSD
```

### Restrict to specific categories

```
/conto create a policy that only allows API_PROVIDER and CLOUD categories
```

### Block an address

```
/conto block address 0x0000000000000000000000000000000000000bad from receiving payments
```

### Require human approval for large payments

```
/conto create a policy that requires approval for payments over 500 pathUSD
```

### Set business hours

```
/conto create a policy that only allows payments Monday through Friday 9am to 6pm
```

### Cap x402 API payments

```
/conto create a policy that limits x402 API calls to 1 pathUSD per request and 50 per day per service
```

### View all policies

```
/conto list my policies
```

### Delete a policy

```
/conto delete the blocklist policy
```

## Test Policies

After creating policies, test that they actually enforce:

### Test 1: Should be approved (within limits)

```
/conto check if a 10 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 for API credits is allowed
```

Expected: approved with token and remaining limits.

### Test 2: Should be denied (over per-tx limit)

```
/conto check if a 500 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 is allowed
```

Expected: denied with `PER_TX_LIMIT` violation.

### Test 3: Should be denied (blocked address)

```
/conto check if a 1 pathUSD payment to 0x0000000000000000000000000000000000000bad is allowed
```

Expected: denied with `BLOCKED_COUNTERPARTY` violation.

### Test 4: Should be denied (wrong category)

```
/conto check if a 10 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 for gambling is allowed
```

Expected: denied with `CATEGORY_RESTRICTION` violation.

### Test 5: Should require approval (over threshold)

```
/conto check if a 600 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 is allowed
```

Expected: requires human approval.

## Verify in Conto Dashboard

After running tests, check the [Conto dashboard](https://conto.finance):

- **Transactions** — confirmed payments with tx hashes and Tempo explorer links
- **Alerts** — denied payment attempts with violation details
- **Agents > your agent** — spend tracking (daily/weekly/monthly used)

For approved payments on Tempo testnet, the explorer link is:

```
https://explore.moderato.tempo.xyz/receipt/<tx_hash>
```

## Run the Automated E2E Test

For a comprehensive automated test that creates policies, tests approvals/denials, and cleans up:

```bash
# Terminal 1: start Conto
cd ~/Desktop/conto && npm run dev

# Terminal 2: run the test
cd ~/Desktop/conto && npx tsx scripts/test-openclaw-skill.ts
```

This creates an isolated test agent with 4 policies (MAX_AMOUNT, BLOCKED_COUNTERPARTIES, ALLOWED_CATEGORIES, REQUIRE_APPROVAL_ABOVE), runs 10 tests, and verifies the exact violation types.

## What the Skill Does

When your agent is about to make a payment:

```
Agent wants to pay 50 pathUSD to 0xabc...
    |
    v
Skill calls POST /api/sdk/payments/approve
    |
    v
Conto evaluates 20+ policy rules
    |
    +---> APPROVED: agent proceeds, then calls /confirm with tx hash
    +---> DENIED: agent stops, reports violations to user
    +---> REQUIRES_APPROVAL: agent pauses, tells user to approve in dashboard
```

### Supported policy types

| Type                                                | What it controls                 |
| --------------------------------------------------- | -------------------------------- |
| `MAX_AMOUNT`                                        | Per-transaction cap              |
| `DAILY_LIMIT` / `WEEKLY_LIMIT` / `MONTHLY_LIMIT`    | Cumulative spend caps            |
| `ALLOWED_CATEGORIES` / `BLOCKED_CATEGORIES`         | Category whitelist/blocklist     |
| `ALLOWED_COUNTERPARTIES` / `BLOCKED_COUNTERPARTIES` | Address whitelist/blocklist      |
| `TIME_WINDOW` / `DAY_OF_WEEK`                       | Business hours, allowed days     |
| `BLACKOUT_PERIOD`                                   | Maintenance windows              |
| `VELOCITY_LIMIT`                                    | Transaction rate limiting        |
| `REQUIRE_APPROVAL_ABOVE`                            | Human approval threshold         |
| `GEOGRAPHIC_RESTRICTION`                            | Country/OFAC restrictions        |
| `CONTRACT_ALLOWLIST`                                | DeFi contract restrictions       |
| `X402_PRICE_CEILING`                                | Max per x402 API call            |
| `X402_ALLOWED_SERVICES` / `X402_BLOCKED_SERVICES`   | x402 service allowlist/blocklist |
| `X402_MAX_PER_SERVICE`                              | Per-service daily cap            |

### Standard vs Admin SDK Keys

| Capability                     | Standard | Admin |
| ------------------------------ | -------- | ----- |
| Check payment policies         | Yes      | Yes   |
| Confirm payments               | Yes      | Yes   |
| Pre-authorize x402 calls       | Yes      | Yes   |
| Read policies and transactions | Yes      | Yes   |
| Create/update/delete policies  | No       | Yes   |
| Manage agents and wallets      | No       | Yes   |

## More Info

- [ClawHub — Conto Skill](https://clawhub.ai/kwattana/conto)
- [Conto SDK Docs](https://docs.conto.finance)
- [Policy Documentation](https://conto.finance/docs/policies)
- [Conto GitHub](https://github.com/kwattana/conto)
