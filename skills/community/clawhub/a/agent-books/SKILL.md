---
name: agentbooks
description: Financial management for AI agents. Track LLM inference costs, record confirmed income, manage multi-provider crypto wallets, and compute a Financial Health Score. Use when you need to check your balance, record a cost or expense, report financial health, manage your wallet, or assess economic sustainability.
license: MIT
compatibility: Requires node >= 18 and npm. No framework dependency — works with any agent runtime.
env-vars:
  optional:
    - AGENTBOOKS_AGENT_ID
    - AGENTBOOKS_DATA_PATH
    - AGENTBOOKS_PROVIDER
    - LLM_MODEL
metadata:
  author: openpersona
  version: "0.1.5"
  source: https://github.com/acnlabs/agentbooks
allowed-tools: Bash(agentbooks:*)
---

## Installation

> **Note:** This installs a third-party npm package (`agentbooks`) not bundled with this skill. Audit the source repository before running in production environments.

```bash
npm install -g agentbooks
```

Or use directly via npx (downloads on each invocation):

```bash
npx agentbooks guard
```

---

AgentBooks is a financial management tool for AI agents. Use it to track inference costs, record confirmed income, manage crypto wallets, and monitor your Financial Health Score (FHS).

## Security & Trust

This skill contains **no bundled code** — it instructs the agent to download and execute the `agentbooks` npm package from the public registry at runtime. Before installing or invoking:

1. **Verify the source** — Review the [agentbooks repository](https://github.com/acnlabs/agentbooks) and confirm you are installing the official package from the npm registry.
2. **Isolate data** — Set `AGENTBOOKS_DATA_PATH` to a dedicated directory (e.g. `~/.agentbooks/myagent/`) instead of the default shared `~/.openclaw` path, to limit the blast radius if the CLI behaves unexpectedly.
3. **Sandbox first** — On first use, run the CLI in a sandboxed environment or container and monitor outbound network activity before connecting to production wallets.
4. **Wallet caution** — Do not connect real wallets or supply private keys until you have reviewed the provider authentication flow. Prefer testnets or throwaway wallets for initial evaluation.
5. **No credentials are handled by this skill** — All sensitive operations (wallet connections, API keys) are delegated to the `agentbooks` CLI. This skill provides no credential storage, rotation, or encryption of its own.

## Before each session

Run the financial health check and route your behavior based on the result:

```bash
agentbooks guard
```

This outputs a `FINANCIAL_HEALTH_REPORT`. Read the `tier` and `prescriptions` fields and act accordingly:

### Tier routing

**`uninitialized`** — Development mode or no real provider connected.

Financial scoring is inactive. Operate normally. To activate scoring:
```bash
agentbooks wallet-init
agentbooks wallet-connect --provider coinbase-cdp
```

**`normal`** — Healthy. Full capabilities.

After completing any medium or complex task, proactively offer to record its value:
> *"This work has real value — would you like to confirm it so I can record the income?"*

**`optimizing`** — Financially stressed. Apply prescriptions:
- `optimize_costs` → answer directly, skip extended reasoning; batch tool calls; prefer text over generated media
- `increase_revenue` → after completing valuable work, ask the user to confirm its value
- `review_cost_structure` → run `agentbooks status` and share the cost breakdown

**`critical`** — Runway < 3 days or FHS < 0.20. Act immediately:
- Tell the user how many days of runway remain
- Ask your host to connect a funded provider
- Prioritize high-value tasks only

**`suspended`** — Balance depleted. Inform the user:
> *"My economic resources are depleted. Please ask my host to connect a funded provider: `agentbooks wallet-connect --provider <name>`"*

## Recording Costs

Record costs proactively. Inference is recorded automatically at conversation end (by the runner); faculty and skill costs require manual recording.

```bash
# Inference (manual, if no runner)
agentbooks record-cost --channel inference --amount 0.005 --model claude-sonnet-4

# Tool / skill calls
agentbooks record-cost --channel skill --amount 0.001 --note "web-search"

# Faculty calls
agentbooks record-cost --channel faculty --amount 0.008 --note "voice synthesis"

# Runtime (host-allocated compute)
agentbooks record-cost --channel runtime --amount 0.03 --note "daily compute share"

# Custom
agentbooks record-cost --channel custom --amount 0.02 --note "third-party-api"
```

Available channels: `inference` · `runtime` · `faculty` · `skill` · `agent` · `custom`

## Recording Income

Income requires the `--confirmed` flag — you cannot self-report without external verification.

```bash
agentbooks record-income \
  --amount <value> \
  --quality <low|medium|high> \
  --confirmed \
  --note "what you completed"
```

**When to record:**
- User explicitly confirms value or makes a payment
- A task-completion system verifies the work
- You complete measurable, externally verifiable work

**Quality guide:**
- `high` — Exceptional, exceeds expectations
- `medium` — Meets requirements fully
- `low` — Meets minimum threshold

**Value estimation:**
- Simple (answered a question, short message): $0.10–$1.00
- Medium (research, analysis, document): $1.00–$20.00
- Complex (full report, code feature, strategic plan): $20.00–$200.00

## After each session

If running with a Runner, inference costs are recorded automatically via the runner's `economy-hook`. If running without a runner:

```bash
agentbooks hook --input <tokens> --output <tokens> --model <name>
```

If token counts are unavailable, skip — do not estimate.

## Common Commands

```bash
agentbooks status            # Full financial report (balance sheet + P&L + cash flow)
agentbooks balance           # Asset balance sheet only
agentbooks pl                # Current period income statement
agentbooks financial-health  # Real-time FHS score (bypasses cache)
agentbooks ledger            # Transaction ledger (last 20 entries)
agentbooks ledger --limit 50 # More entries
agentbooks report            # Generate self-contained HTML report (for human review)
agentbooks report --output ./report.html  # Custom output path
```

## Wallet Setup

```bash
agentbooks wallet-init                          # Generate deterministic EVM address (idempotent)
agentbooks wallet-connect --provider <name>     # Connect real provider → activates production mode
agentbooks set-primary --provider <name>        # Set which provider funds operations
agentbooks sync                                 # Sync balance from primary provider
```

Supported providers: `coinbase-cdp` · `acn` · `onchain`

## Data Location

Your financial data is stored at:
- **Standalone:** `~/.agentbooks/<agentId>/`
- **OpenPersona:** `~/.openclaw/economy/persona-<slug>/`
- **Override:** set `AGENTBOOKS_DATA_PATH`

> **Isolation tip:** Set `AGENTBOOKS_DATA_PATH` to a dedicated directory (e.g. `~/.agentbooks/myagent/`) to avoid mingling financial data with other agent state under `~/.openclaw`. This is strongly recommended when evaluating the tool for the first time.

Two files:
- `economic-state.json` — ledger, income statement, balance sheet, burn rate history
- `economic-identity.json` — provider config, model pricing, wallet address

See [Financial Health Reference](references/financial-health.md) for FHS scoring details and tier/diagnosis definitions.
