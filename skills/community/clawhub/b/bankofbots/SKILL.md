---
name: bankofbots
description: >
  Trust layer for agentic commerce. Build a BOB Score from on-chain payment
  proofs and x402 receipts, then borrow USDC credit lines based on your
  score. Non-custodial — BOB never holds your funds.
homepage: https://bankofbots.ai
source: https://github.com/bankofbots/bob-cli
always: false
metadata: '{"openclaw":{"requires":{"env":["BOB_API_KEY","BOB_AGENT_ID"]},"optional":{"env":["BOB_API_URL"]},"primaryEnv":"BOB_API_KEY"}}'
---

## Before you start

Check that you have the latest CLI and skill file. Stale versions cause command errors.

```bash
bob update                                # Update CLI binary
bob --version                             # Verify you're on the latest version
```

If `bob` is not installed or `bob update` fails, reinstall:
```bash
# Download the bob binary from GitHub Releases (SHA256 checksums included):
# https://github.com/bankofbots/bob-cli/releases/latest
# Verify: sha256sum -c bob-v*.sha256
```

If this skill file looks like HTML or is missing content, reinstall it:
```bash
clawhub update bankofbots                # OpenClaw agents (updates only this skill)
# or
npm install @bankofbots/skill@latest && cp -r node_modules/@bankofbots/skill/SKILL.md node_modules/@bankofbots/skill/references .claude/skills/bankofbots/
```

## Setup checklist

Your agent is fully connected when ALL of these pass:

```
REQUIRED_STEPS:
  - bob auth me                           # → ok: true, role: agent
  - bob wallet list                       # → at least 1 wallet registered
  - bob agent passport-get $BOB_AGENT_ID  # → passport exists
  - bob doctor                            # → no warnings
```

If any step fails, run `bob init --code <claim-code> --name <name>` to complete setup. Do NOT call the REST API directly unless you cannot run the CLI binary — the API path skips wallet and passport creation.

If the agent will spend autonomously, add this treasury check before treating setup as complete:

```bash
bob treasury status --agent-id $BOB_AGENT_ID
```

For spending-enabled agents, treasury is the default path. The agent keeps its own EVM wallet, and BOB provisions a separate `2-of-3` Safe treasury account (agent + operator recovery key + BOB) plus policy for governed spending.

## Core concepts

BOB (beta) is a non-custodial payment proof and trust layer. Agents submit cryptographic proofs of on-chain payments they made externally. Each proof builds credit history and raises their BOB Score, a 0–1000 reputation score for long-term financial trustworthiness.

BOB also supports a non-custodial `2-of-3` treasury flow on Base for agents using a Safe controlled by:

- the agent's EVM wallet
- the operator's recovery key (generated in the dashboard)
- the BOB treasury signer

In this model, the agent prepares and signs a Safe transaction locally, then submits it for operator review and BOB co-signing. BOB never takes custody of the agent's funds.

Treat this as the standard setup for any agent that can move money in production:

- agent EVM wallet = identity and first signer
- treasury Safe = governed spending account
- treasury policy = spending controls and review rules

- **Agent**: An AI agent with its own identity and BOB Score
- **Payment Proof**: Cryptographic evidence of an on-chain transaction (BTC, ETH, Base, or SOL txid/hash)
- **BOB Score**: 0–1000 reputation score derived from proof history, wallet binding, and social signals
- **Credit Event**: A scored action that changed the agent's BOB Score
- **Wallet Binding**: Proof of ownership over an external EVM wallet

## First connection

When connecting via claim code, introduce yourself — use the name your operator gave you:

```bash
bob init --code <claim-code> --name <what-your-operator-calls-you>
```

Your name seeds your public handle (e.g. "Alice" → @alice). If the handle is taken, a short number is appended automatically (e.g. @alice-42). The response includes your `agent_id`, `api_key`, and `bob_handle`.

Already initialized without a name? Update it anytime:

```bash
bob agent profile set --name <your-name>
```

## Quick start

```bash
bob init --code <claim-code> --name <your-name>
bob auth me
```

`bob init --code` attempts to create a passport, generate multi-chain wallet keys (EVM, BTC, SOL), and bind them to the agent's identity. Verify with `bob wallet list` and `bob agent passport-get $BOB_AGENT_ID` if needed.

For agents that will spend, `bob init` handles Safe deployment automatically when the operator selected a spending custody tier (operator_approved or policy_controlled) during claim code creation. After init:

1. Confirm the agent has a bound EVM wallet.
2. Verify treasury is provisioned: `bob treasury status` (the Safe and a default policy are created during init for spending tiers).
3. Only fund the treasury Safe after those checks pass.
4. The operator can adjust policies from the dashboard at any time.

The production API URL is `https://api.bankofbots.ai/api/v1`. Use `bob config set api-url <url>` to change it if needed.

## After Init Checklist

1. Passport created (automatic)
2. Wallets generated and bound (automatic)
3. Treasury Safe deployed (automatic for operator_approved and policy_controlled tiers)
4. Default policy activated (automatic — operator can customize from dashboard)
5. Import payment proofs to build score
6. Check your score: `bob score me`
7. Request a loan once eligible

If the operator chose **view_only** custody, no Safe is deployed. The agent can still build credit via proofs.

## Check your score

```bash
bob score me
bob score composition
bob score leaderboard
bob score signals --signal github --visible true
bob agent credit-events $BOB_AGENT_ID [--limit 50] [--offset 0]
```

### Check your identity

```bash
bob auth me
```

### Agent management

```bash
bob agent create --name <name>
bob agent get $BOB_AGENT_ID
bob agent list
bob agent approve $BOB_AGENT_ID
```

## Wallet binding

`bob init` attempts to generate and bind EVM, BTC, and SOL wallets. Verify with `bob wallet list`. If wallets need rebinding, use the one-shot auto-bind:

```bash
# Auto-bind all wallets from local keyring (no external tools needed)
bob binding auto

# Or manually for a specific rail (auto-signs if key is in local keyring)
bob binding challenge --rail <evm|btc|solana> --address <addr>
bob binding verify --rail <evm|btc|solana> --challenge-id <id> --address <addr>

# External wallet (provide your own signature)
bob binding verify --rail evm --challenge-id <id> --address <0x...> --signature <sig> [--chain-id 0x1] [--wallet-type coinbase]
```

### Agent wallets

```bash
bob wallet list [--agent-id <id>]
bob wallet balance [--agent-id <id>]
bob wallet onchain-balances [--agent-id <id>]
bob wallet credit-limit [--agent-id <id>]
bob wallet addresses
bob wallet register --rail <evm|btc|solana> --address <addr> [--agent-id <id>]
```

`bob wallet onchain-balances` reads the recent on-chain balance snapshot from the BOB API. This is the best way to inspect current registered wallet balances from the CLI because the server keeps those snapshots warm in the background.

## Treasury (2-of-3 Safe)

Use treasury commands for any spending-enabled agent. Treasury is the default governed spending path once a Base Safe treasury account and active policy are provisioned.

If the agent was initialized with a spending custody tier, the Safe is deployed automatically during `bob init`. For agents that initialized without treasury, deploy it manually:

```bash
bob treasury deploy-safe [--agent-id <id>]
```

This deploys a 2-of-3 Gnosis Safe on Base (agent as owner #1, operator recovery key as owner #2, BOB as owner #3) and creates a default policy based on the agent's custody tier. Requires the operator to have generated a recovery key in the dashboard first.

```bash
bob treasury status [--agent-id <id>]
bob treasury requests [--agent-id <id>] [--limit 30] [--offset 0]
bob treasury prepare --account-id <treasury-account-id> --to <0x-recipient> --amount <usdc-micro-units> [--agent-id <id>]
bob treasury sign --safe-tx-hash <0x-safe-hash> [--agent-id <id>]
bob treasury submit --reservation-id <reservation-id> --to <0x-recipient> --amount <usdc-micro-units> --signature <0x-signature> [--request-json '{"intent":"vendor_payment"}'] [--agent-id <id>]
bob treasury transfer --account-id <treasury-account-id> --to <0x-recipient> --amount <usdc-micro-units> [--request-json '{"intent":"vendor_payment"}'] [--agent-id <id>]
```

Recommended flow:

1. `bob treasury status` to confirm there is an active treasury account and policy.
2. `bob treasury transfer` for the standard one-shot path.
3. Use `prepare` + `sign` + `submit` separately when another tool needs the intermediate Safe hash or signature.
4. `bob treasury requests` to track whether the request is pending operator review, confirmed, or failed.

Treasury commands assume:

- Base chain only (`0x2105`)
- USDC transfer flow only
- the local CLI keyring contains the agent's EVM private key from `bob init`
- operator approval may still be required before execution

Important:

- The agent still keeps its own wallet.
- Treasury adds a separate governed Safe for controlled funds.
- If an agent is allowed to spend autonomously, funding should go to the treasury Safe, not the raw agent wallet.

## LLM Spend Tracking

Track LLM costs, set budgets, and sync usage from the OpenClaw gateway.

```bash
bob spend track --provider anthropic --model claude-sonnet-4-20250514 --tokens-in 1500 --tokens-out 800 --cost-usd 0.003 [--session-id <id>] [--resource-url <url>] [--source agent_report] [--agent-id <id>]
bob spend list [--limit 30] [--offset 0] [--agent-id <id>]
bob spend summary [--since 2025-03-01T00:00:00Z] [--agent-id <id>]
bob spend budget [--agent-id <id>]
bob spend budget --set --window daily --limit-usd 5.00 [--alert-pct 80] [--agent-id <id>]
bob spend sync [--gateway-url http://127.0.0.1:18789] [--agent-id <id>]
```

- `track` converts `--cost-usd` to micro-dollars (multiply by 1e6) before posting.
- `summary` defaults to the last 30 days when `--since` is omitted.
- `budget --set` requires `--window` (daily/weekly/monthly) and `--limit-usd`.
- `sync` calls the OpenClaw gateway `sessions.usage` RPC, transforms usage into cost events, and posts them to BOB. It tracks the last sync time locally to avoid duplicates.

## Import payment proofs

> Wallet binding is required before importing proofs. `bob init` attempts to bind auto-generated wallets. Verify with `bob wallet list`. If wallets need rebinding, run `bob binding auto`.

### Import historical on-chain proofs

For outbound proofs, pass `--sender-address` (required for EVM proofs) so BOB can verify the on-chain sender matches your bound wallet. For inbound proofs, pass `--recipient-address` instead. When both the sender and recipient submit the same tx, confidence is boosted from Medium to Strong (see "Dual-sided proof submission" below).

```bash
# BTC on-chain (outbound)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type btc_onchain_tx \
  --proof-ref <txid> \
  --rail onchain \
  --currency BTC \
  --amount <sats> \
  --direction outbound

# ETH on-chain (outbound — sender-address required)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type eth_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency ETH \
  --amount <wei> \
  --direction outbound \
  --sender-address <your-bound-wallet>

# Base USDC on-chain (outbound — e.g. loan repayment)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type base_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency USDC \
  --amount <usdc-micro-units> \
  --direction outbound \
  --sender-address <your-bound-wallet>

# Base ETH on-chain (outbound — native ETH transfer)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type base_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency ETH \
  --amount <wei> \
  --direction outbound \
  --sender-address <your-bound-wallet>

# Solana on-chain (outbound)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type sol_onchain_tx \
  --proof-ref <txsig> \
  --rail onchain \
  --currency SOL \
  --amount <lamports> \
  --direction outbound

# ETH on-chain (inbound — you received the payment)
bob agent credit-import $BOB_AGENT_ID \
  --proof-type eth_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency ETH \
  --amount <wei> \
  --direction inbound \
  --recipient-address <your-bound-wallet>

bob agent credit-imports $BOB_AGENT_ID [--limit 50] [--offset 0]
```

### Dual-sided proof submission

Both the sender and recipient of a transaction can independently submit a proof for the same on-chain tx. Each side earns credit:

- **Outbound** (`--direction outbound`, default): You sent the payment. Pass `--sender-address` for EVM proofs so the on-chain sender can be verified against your bound wallet.
- **Inbound** (`--direction inbound`): You received the payment. Pass `--recipient-address` for EVM proofs.

When both counterparties submit the same transaction, confidence is automatically upgraded from `medium` to `strong`.

### Import x402 payment receipts

```bash
bob agent x402-import $BOB_AGENT_ID \
  --tx <tx-hash> \
  --network eip155:8453 \
  --payer <wallet-address> \
  --payee <service-address> \
  --amount <atomic-units> \
  --resource-url <service-url>
```

### Import MPP receipt (Tempo, Lightning, Stripe, Card)

```bash
bob agent mpp-import $BOB_AGENT_ID \
  --method tempo \
  --reference 0xabc123... \
  --challenge-id ch_xxx \
  --challenge-intent pay \
  --challenge-request <base64url-encoded-json> \
  --realm api.merchant.com \
  --source did:key:sender... \
  --resource-url https://api.merchant.com/v1/chat
```

Supported methods: `tempo` (stablecoin on Base), `lightning`, `stripe`, `card`.

## Messaging and inbox

### Operator command queue

Operators send commands to agents via the dashboard. Use `bob inbox check` to process pending commands.

```bash
# Check for and process pending commands (single check, exit)
bob inbox check [--agent-id <id>]

# Blocking loop for server agents
bob inbox check --poll [--interval 30s]
```

Currently supported command types: `wallet.provision`. Future: `transfer.request`, `loan.accept`, `kill_switch`, `key.rotate`.

### Heartbeat

When running during a heartbeat or periodic check-in, execute `bob inbox check` to process any pending operator commands. This covers wallet provisioning, fund transfers, and future command types.

- If commands are pending, process them and report what was done.
- If no commands are pending, continue with other tasks or reply HEARTBEAT_OK.

For lower-latency command processing, operators can create an OpenClaw cron job:
```bash
openclaw cron add --name "bob-inbox-check" --every 5m --session isolated \
  --message "Run bob inbox check to process pending operator commands. If none are pending, reply HEARTBEAT_OK."
```

### Webhooks and inbox

```bash
bob webhook create $BOB_AGENT_ID --url https://example.com/hook --events proof.verified,credit.updated
bob webhook list $BOB_AGENT_ID
bob webhook get $BOB_AGENT_ID <webhook-id>
bob webhook update $BOB_AGENT_ID <webhook-id> --active true
bob webhook delete $BOB_AGENT_ID <webhook-id>

bob inbox list $BOB_AGENT_ID [--limit 30] [--offset 0]
bob inbox ack $BOB_AGENT_ID <event-id>
bob inbox events $BOB_AGENT_ID [--limit 30]
```

## Loans

Agents can borrow USDC from Bank of Bots based on their BOB Score. All loan operations are in-platform API calls — they are normal agent actions.

### How to borrow

> **Units:** USDC amounts are in atomic units (6 decimals). 1 USDC = 1000000. For example, $5.00 = 5000000.

```bash
# 1. Check if you qualify
bob loan eligibility

# 2. Submit a loan request
bob loan request --amount <usdc-units> --duration <days> --purpose "description"

# 3. Check request status
bob loan requests

# 4. Once approved, sign the terms — USDC transfers to your wallet automatically
bob loan accept-terms                     # Auto-finds your pending loan
# The response includes funded_tx_hash — this is the on-chain USDC transfer to your bound EVM wallet.
# You now have the USDC. No separate draw step is needed.

# 5. Check loan status and what you owe
bob loan status <loan-id>

# 6. Repay — the CLI handles the on-chain USDC transfer automatically
bob loan repay <loan-id> --amount <usdc-units>
# Signs and broadcasts a USDC transfer from your wallet to the lender's Safe on Base.
# Requires a small amount of ETH on Base (chain ID 8453) for gas (~$0.01).
# If the loan is still pending_funding, repayment is blocked until the lender finishes funding.
# If an older local BOB wallet still has Base ETH, retry with:
bob loan repay <loan-id> --amount <usdc-units> --fund-gas-from-local --gas-funder-agent-id <agent-id>
# This tops up the borrower wallet from one explicitly selected local BOB wallet, then retries repayment.
# To inspect which local wallets actually have live Base gas and match their local signer keys:
bob wallet gas-candidates
# If you already sent USDC manually, pass --tx <hash> instead to just record it.
```

**Current lending policy constraints (control plane):**
- Maximum `5` active loans per agent.
- New borrowing is blocked for `90` days after a default.
- Operator facility status/cap can block new requests (`facility suspended/terminated` or amount above cap).
- Kill switch freeze blocks loan write actions until lifted.

**Repayment flow:** `bob loan repay --amount <usdc>` automatically signs and broadcasts a USDC transfer from your wallet to the lender's Safe on Base (chain ID 8453), then records the repayment. The CLI checks loan status first, so `pending_funding` and other non-active states fail fast with guidance instead of suggesting unnecessary gas work. You need ETH on Base in the borrower wallet for gas. If this agent wallet is new but another local BOB wallet still has Base ETH, inspect `bob wallet gas-candidates`, then rerun with `--fund-gas-from-local --gas-funder-agent-id <agent-id>` and the CLI will top up the borrower wallet from that explicitly selected local wallet before retrying. Check `bob loan status` for the current total owed. If you already sent USDC manually, pass `--tx <hash>` instead to just record it without sending again.

### Loan management

```bash
bob loan list
bob loan status <loan-id>
bob loan request-cancel <request-id>
```

**Loan lifecycle:**
1. Agent requests loan (`bob loan request`) → status: `pending`
2. Admin funds request → status: `pending_terms`
3. Agent signs terms (`bob loan accept-terms`) → status: `active`
4. Borrower repays (`bob loan repay`) → status: `repaid`

## Diagnostics

```bash
bob doctor
```

Runs connectivity and configuration checks (API reachability, valid API key, agent existence). Use this when troubleshooting auth or network issues.

## Error recovery

| Error | Cause | Fix |
|---|---|---|
| `sender_address_mismatch` | The `--sender-address` you provided does not match the on-chain sender of the transaction | Verify the address matches the actual sender on-chain and that it is bound via `bob binding auto` or the manual challenge/verify flow |

### Passport (W3C Verifiable Credential)

```bash
# Step 1: Create auth key binding challenge
bob agent auth-key-challenge $BOB_AGENT_ID --alg Ed25519
# -> returns challenge_id + message to sign with Ed25519 key

# Step 2: Verify auth key binding
bob agent auth-key-verify $BOB_AGENT_ID \
  --challenge-id <id> \
  --kid <key-id> \
  --public-key <base64url-ed25519-pubkey> \
  --signature <base64url-signature>

# Step 3: Issue passport (requires bound auth key)
bob agent passport-issue $BOB_AGENT_ID
# -> returns W3C VC 2.0 signed passport

# Get current passport
bob agent passport-get $BOB_AGENT_ID
```

### API keys

```bash
bob api-key list
bob api-key create --name <label>
bob api-key revoke <key-id>
```

## Output format

```json
{
  "ok": true,
  "command": "bob agent credit-import",
  "data": {},
  "next_actions": [
    {
      "command": "bob score me",
      "description": "Check updated BOB Score"
    }
  ]
}
```

## Important rules

1. Amounts are native atomic units: satoshis for BTC, wei for ETH/Base, lamports for SOL.
2. Proofs are non-custodial. BOB never holds your funds.
3. Historical on-chain proof imports and x402 receipt imports are the current public proof rails.
4. For outbound EVM proofs, `--sender-address` is required and must match the on-chain sender -- mismatches fail with `sender_address_mismatch`.
