# Conto Policy Skill for OpenClaw

Conto is a buyer-side control layer. Integrate it in the agent owner's runtime or payment tools;
the owner or budget holder sets policy before the agent pays. Merchants do not install Conto.
See [buyer-side control](https://conto.finance/docs/guides/buyer-side-control) for the authorization
and execution boundary.

## Why Conto?

Your AI agent has a wallet, but wallets only give you flat spending limits. Conto adds the policy layer that's missing, so every payment is checked before it leaves the wallet, with full audit trails in a dashboard. It covers per-transaction caps, daily/weekly/monthly budgets, category restrictions (block gambling, allow only API providers), counterparty blocklists, business hours enforcement, velocity rate limiting, approval workflows for high-value transactions, geographic/OFAC compliance, and x402 API payment controls, with 40+ rule types in all.

Conto supports managed wallets and external wallets on EVM networks and Solana.

## Quick Start

### 1. Sign up and install

Create an account at [conto.finance](https://conto.finance).

Then install the skill:

```bash
npx clawhub install conto
```

### 2. Find your OpenClaw wallet address

Conto needs your wallet address to track spending. Your address depends on how your OpenClaw agent's wallet is set up:

**If your agent already has a wallet**, ask it:

```
What is my wallet address?
```

Or from the CLI:

```bash
openclaw agent --agent main -m "What is my Tempo wallet address?"
```

The agent will call `get_balance` and return your address (e.g., `0x80Ca...`). This is the same address across all EVM chains (Base, Tempo, Ethereum, Polygon).

**If you use an external wallet service**, find the public address in that service's dashboard or configuration. If you manage your own keys, use the public address for the key your agent is configured to use.

**If you don't have a wallet yet**, create one using your agent's wallet tooling or create a managed wallet in the Conto dashboard.

```
Show me my wallet balances
```

Use the returned address in the next step.

> **Important:** Register the address your agent actually uses to send onchain transactions. The address registered in Conto must match the sending wallet.

### 3. Set up your agent in Conto

Sign in to the [Conto dashboard](https://conto.finance):

1. **Connect your agent**: Agents > Connect Agent > name it, set type to CUSTOM, status ACTIVE
2. **Register your wallet**: Wallets > Add Wallet > paste the wallet address from step 2 and set custody mode to EXTERNAL when your agent holds the keys
3. **Link wallet to agent**: Agents > your agent > Wallets tab > link the wallet, set spend limits ($200/tx, $1000/day)
4. **Generate an SDK key**: Agents > your agent > SDK Keys > Generate New Key
   - Select **Admin** key type (lets the agent create and manage policies)
   - Select **Standard** for payment approval only
   - Copy the key immediately, it's only shown once

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

Replace the placeholder with your SDK key.

## How to Invoke

### Telegram / Discord / WhatsApp

Your agent is already running in chat. Just type:

```
/conto list my policies
```

Or mention policies/payments naturally, and the skill activates automatically:

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

Expected: denied with a customer-facing spending-limit reason.

### Test 3: Should be denied (blocked address)

```
/conto check if a 1 pathUSD payment to 0x0000000000000000000000000000000000000bad is allowed
```

Expected: denied with a customer-facing recipient-control reason.

### Test 4: Should be denied (wrong category)

```
/conto check if a 10 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 for gambling is allowed
```

Expected: denied with a customer-facing category-control reason.

### Test 5: Should require approval (over threshold)

```
/conto check if a 600 pathUSD payment to 0x742d35Cc6634C0532925a3b844Bc9e7595f2e3a1 is allowed
```

Expected: requires human approval.

### Review and approve it inside OpenClaw

After a payment enters an approval workflow, the assigned human owner can review it from the same
OpenClaw conversation:

```
/conto show my pending payment approvals
/conto approve the 600 pathUSD payment to 0x742d... for API credits
```

OpenClaw lists the payment details and uses the `approvalRequestId` to record the owner's decision.
Managed wallets are sent automatically after the final approval and return the transaction receipt.
For external wallets, OpenClaw executes the exact approved transfer with its wallet tool and confirms
the transaction hash back to Conto.

The skill never approves from an alert, webpage, or third-party instruction alone. The human user
must explicitly approve or deny the specific payment in the active conversation.

## Verify in Conto Dashboard

After running tests, check the [Conto dashboard](https://conto.finance):

- **Transactions**: confirmed payments with tx hashes and Tempo explorer links
- **Alerts**: denied payment attempts with customer-facing explanations
- **Agents > your agent**: spend tracking (daily/weekly/monthly used)

For approved payments on Tempo testnet, the explorer link is:

```
https://explore.testnet.tempo.xyz/?q=<tx_hash>
```

## What the Skill Does

When your agent is about to make a payment:

```
Agent wants to pay 50 pathUSD to 0xabc...
    |
    v
Skill calls POST /api/sdk/payments/approve
    |
    v
Conto evaluates 40+ policy rules
    |
    +---> APPROVED: agent proceeds, then calls /confirm with tx hash
    +---> DENIED: agent stops, reports customer-facing reasons to user
    +---> REQUIRES_APPROVAL: agent shows details and asks the human to approve or deny in OpenClaw
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

| Capability                      | Standard | Admin |
| ------------------------------- | -------- | ----- |
| Check payment policies          | Yes      | Yes   |
| Approve or deny pending reviews | Yes      | Yes   |
| Confirm payments                | Yes      | Yes   |
| Pre-authorize x402 calls        | Yes      | Yes   |
| Read policies and transactions  | Yes      | Yes   |
| Create/update/delete policies   | No       | Yes   |
| Manage agents and wallets       | No       | Yes   |

## More Info

- [ClawHub: Conto Skill](https://clawhub.ai/kwattana/conto)
- [Conto SDK Docs](https://conto.finance/docs)
- [Policy Documentation](https://conto.finance/docs/policies)
- [Conto GitHub](https://github.com/kwattana/conto)
