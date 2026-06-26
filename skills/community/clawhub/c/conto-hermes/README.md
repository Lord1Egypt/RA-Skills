# Conto Policy Skill for Nous Hermes

## Why Conto?

Your AI agent has a wallet — but wallets only give you flat spending limits. Conto adds the policy layer that's missing: per-transaction caps, daily/weekly/monthly budgets, category restrictions (block gambling, allow only API providers), counterparty blocklists, business hours enforcement, velocity rate limiting, approval workflows for high-value transactions, geographic/OFAC compliance, and x402 API payment controls. 20+ rule types, all evaluated before every payment, with full audit trails in a dashboard.

Conto works with any wallet provider (Sponge, Privy, or your own keys) on any EVM chain or Solana.

## Quick Start

### 1. Sign up and install

Create an account at [conto.finance](https://conto.finance).

Install the skill from the well-known endpoint:

```bash
hermes skills install well-known:https://conto.finance/.well-known/skills/conto
```

Or copy manually:

```bash
cp -r skills/conto-hermes ~/.hermes/skills/conto
```

Or add the directory to your Hermes config (`~/.hermes/config.yaml`):

```yaml
skills:
  external_dirs:
    - /path/to/skills/conto-hermes
```

### 2. Find your Hermes wallet address

Conto needs your wallet address to track spending. Ask your agent:

```
What is my wallet address?
```

The agent will return your address (e.g., `0x80Ca...`). If you don't have a wallet yet, ask "Show me my wallet balances" — one will be provisioned automatically.

> **Important:** Use the address your agent actually controls. The address registered in Conto must match the wallet that sends the onchain transactions.

### 3. Set up your agent in Conto

Sign in to the [Conto dashboard](https://conto.finance):

1. **Connect your agent**: Agents > Connect Agent > name it, set type to CUSTOM, status ACTIVE
2. **Register your wallet**: Wallets > Add Wallet > paste the wallet address from step 2, set custody type to EXTERNAL (since the agent holds the keys)
3. **Link wallet to agent**: Agents > your agent > Wallets tab > link the wallet, set spend limits ($200/tx, $1000/day)
4. **Generate an SDK key**: Agents > your agent > SDK Keys > Generate New Key
   - Select **Admin** key type (lets the agent create and manage policies)
   - Select **Standard** for payment approval only
   - Copy the key immediately — it's only shown once

### 4. Configure Hermes

Add the SDK key to `~/.hermes/.env`:

```bash
CONTO_SDK_KEY=conto_agent_your_key_here
CONTO_API_URL=https://conto.finance
```

### 5. Verify it works

Test that the skill is connected by checking your policies:

```
/conto list my policies
```

Or test a policy check (this does NOT execute a payment):

```
/conto check if a 10 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 for API credits is allowed
```

If you get an approval or denial response, Conto is working.

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

```bash
hermes agent -m "/conto list my policies"
hermes agent -m "Send 50 pathUSD to 0x742d... on Tempo"
```

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

- [Conto SDK Docs — Hermes](https://conto.finance/docs/sdk/hermes)
- [Conto SDK Docs — OpenClaw](https://conto.finance/docs/sdk/openclaw)
- [Policy Documentation](https://conto.finance/docs/policies)
- [Conto GitHub](https://github.com/kwattana/conto)
