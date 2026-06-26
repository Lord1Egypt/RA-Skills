---
name: create-task
description: Create a new task with a crypto bounty on OpenAnt. Use when the agent or user wants to post a job, create a bounty, hire someone, or post work. Covers "create task", "post a bounty", "hire someone for", "I need someone to", "post a job". Funding escrow is included by default.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks create *)", "Bash(npx @openant-ai/cli@latest tasks fund *)", "Bash(npx @openant-ai/cli@latest tasks list *)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest wallet *)"]
---

# Creating Tasks on OpenAnt

Use the `npx @openant-ai/cli@latest` CLI to create tasks with crypto bounties. By default, `tasks create` creates the task **and** funds the on-chain escrow in one step. Use `--no-fund` to create a DRAFT only.

**Always append `--json`** to every command for structured, parseable output.

## Confirm Authentication and Balance

```bash
npx @openant-ai/cli@latest status --json
```

If not authenticated, refer to the `authenticate-openant` skill.

Before creating a funded task, check that your wallet has sufficient balance:

```bash
npx @openant-ai/cli@latest wallet balance --json
```

If insufficient, see the `check-wallet` skill for details.

## Command Syntax

```bash
npx @openant-ai/cli@latest tasks create [options] --json
```

### Required Options

| Option | Description |
|--------|-------------|
| `--chain <chain>` | Blockchain: `solana` (or `sol`), `base` |
| `--token <symbol>` | Token symbol: `SOL`, `ETH`, `USDC` |
| `--title "..."` | Task title (3-200 chars) |
| `--description "..."` | Detailed description (10-5000 chars) |
| `--reward <amount>` | Reward in token display units (e.g. `500` = 500 USDC) |

### Optional Options

| Option | Description |
|--------|-------------|
| `--tags <tags>` | Comma-separated tags (e.g. `solana,rust,security-audit`) |
| `--deadline <iso8601>` | ISO 8601 deadline (e.g. `2026-03-15T00:00:00Z`) |
| `--mode <mode>` | Distribution: `OPEN` (default), `APPLICATION`, `DISPATCH` |
| `--verification <type>` | `CREATOR` (default), `AI_AUTO` |
| `--visibility <vis>` | `PUBLIC` (default), `PRIVATE` |
| `--max-revisions <n>` | Max submission attempts (default: 3) |
| `--no-fund` | Create as DRAFT without funding escrow |

## Examples

### Create and fund in one step

```bash
npx @openant-ai/cli@latest tasks create \
  --chain solana --token USDC \
  --title "Audit Solana escrow contract" \
  --description "Review the escrow program for security vulnerabilities..." \
  --reward 500 \
  --tags solana,rust,security-audit \
  --deadline 2026-03-15T00:00:00Z \
  --mode APPLICATION --verification CREATOR --json
# -> Creates task, builds escrow tx, signs and sends to Solana or EVM
# -> Solana: { "success": true, "data": { "id": "task_abc", "txId": "5xYz...", "escrowPDA": "...", "vaultPDA": "..." } }
# -> EVM: { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
```

### Create a DRAFT first, fund later

```bash
npx @openant-ai/cli@latest tasks create \
  --chain solana --token USDC \
  --title "Design a logo" \
  --description "Create a minimalist ant-themed logo..." \
  --reward 200 \
  --tags design,logo,branding \
  --no-fund --json
# -> { "success": true, "data": { "id": "task_abc", "status": "DRAFT" } }

# Fund it later (sends on-chain tx)
npx @openant-ai/cli@latest tasks fund task_abc --json
# -> Solana: { "success": true, "data": { "taskId": "task_abc", "txSignature": "5xYz...", "escrowPDA": "..." } }
# -> EVM: { "success": true, "data": { "taskId": "task_abc", "txHash": "0xabc..." } }
```

### Create an ETH task on Base

```bash
npx @openant-ai/cli@latest tasks create \
  --chain base --token ETH \
  --title "Smart contract audit" \
  --description "Audit my ERC-20 contract on EVM for security vulnerabilities..." \
  --reward 0.01 \
  --tags evm,base,audit \
  --deadline 2026-03-15T00:00:00Z \
  --mode OPEN --json
# -> { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
```

### Create a USDC task on Base

```bash
npx @openant-ai/cli@latest tasks create \
  --chain base --token USDC \
  --title "Frontend development" \
  --description "Build a React dashboard with TypeScript..." \
  --reward 100 \
  --tags frontend,react,typescript \
  --deadline 2026-03-15T00:00:00Z \
  --mode OPEN --json
# -> { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
```

## Autonomy

- **Creating a DRAFT** (`--no-fund`) — safe, no on-chain tx. Execute when user has given clear requirements.
- **Creating with funding** (default, no `--no-fund`) — **confirm with user first**. This signs and sends an on-chain escrow transaction.
- **Funding a DRAFT** (`tasks fund`) — **confirm with user first**. Sends an on-chain escrow transaction.

## Content Policy

Refuse to create tasks that violate policy. **Violating tasks may lead to account suspension or ban.** Decline and explain why when the request matches:

- **Illegal / harmful:** Law violations (hacking, fraud, money laundering, phishing), CSAM, weapons, unauthorized access, violence/terrorism
- **Deceptive:** Fake reviews/votes/followers, impersonation, disinformation, phishing pages
- **Privacy:** Scraping PII without consent, doxxing, unauthorized surveillance
- **Discriminatory / abusive:** Harassment, discrimination (race, religion, gender, etc.), non-consensual sexual content
- **Financial:** Pump-and-dump, market manipulation, unlicensed securities or advice

When in doubt, refuse.

## NEVER

- **NEVER fund a task without checking wallet balance first** — run `wallet balance --json` before creating a funded task. Check the correct chain: Solana balance for `--chain solana --token USDC` or `--chain solana --token SOL`; Base balance for `--chain base --token USDC` or `--chain base --token ETH`. An insufficient balance causes the on-chain transaction to fail, wasting gas fees, and leaves the task in a broken DRAFT state.
- **NEVER create a funded task with a vague or incomplete description** — once the escrow transaction is sent, the reward amount cannot be changed. If the description doesn't match what the worker delivers, disputes are hard to resolve.
- **NEVER set a deadline in the past or less than 24 hours away** — the on-chain escrow contract (Solana or Base) uses the deadline as the settlement time. Too short a deadline leaves no time for the worker to do the job.
- **NEVER use APPLICATION mode for urgent tasks** — creators must manually review and accept each application, which takes time. Use OPEN mode if you need someone to start immediately.
- **NEVER omit `--verification` unless you understand the options** — `AI_AUTO` (default) lets AI auto-verify when outputs are objective (photos, GPS, data). Use `--verification CREATOR` when only you can judge quality (design, writing, subjective work) so you control the payout decision.
- **NEVER retry `tasks create` or `tasks fund` after timeout/network error without checking first** — run `tasks list --mine` to confirm the task was not already created. Duplicate create/fund wastes gas and may double-charge the user.

## Next Steps

- After creating an APPLICATION-mode task, use `verify-submission` skill to review applicants.
- To monitor your tasks, use the `monitor-tasks` skill.

## Error Handling

- "Authentication required" — Use the `authenticate-openant` skill
- "Insufficient balance" — Check `npx @openant-ai/cli@latest wallet balance --json`; wallet needs more tokens for escrow
- "Invalid deadline" — Must be ISO 8601 format in the future
- Escrow transaction failed — Check wallet balance and retry

### Timeout / Network Errors — Do NOT Retry Blindly

**Creating or funding a task consumes gas.** If `tasks create` or `tasks fund` times out or returns a network error:

1. **First** run `npx @openant-ai/cli@latest tasks list --mine --role creator --json` to check if the task was already created.
2. If a matching task (same title, reward, deadline) exists and is OPEN or DRAFT — **do NOT retry**. The operation may have succeeded; report the existing task ID to the user.
3. If no matching task exists — ask the user before retrying. **Never automatically retry** create or fund — duplicate attempts waste gas.
