---
name: elytro
description: >
  Elytro smart-account wallet CLI for agents: multi-chain ERC-4337, 2FA email OTP, spending limits,
  social recovery. Simulate before send, get user approval on risky steps, and explain outcomes in a
  fixed, user-friendly format (no raw JSON unless asked). Deferred OTP completed with otp submit.
  Use for: accounts, transfers, contract calls, email/security setup, guardian recovery. Node >= 24.
version: 0.7.3
homepage: https://elytro.com
metadata:
  openclaw:
    requires:
      bins:
        - elytro
      node: ">=24.0.0"
    emoji: "🔐"
    homepage: https://github.com/Elytro-eth/skills
    os: ["macos", "windows", "linux"]
    install:
      - id: npm
        kind: npm
        package: "@elytro/cli"
        bins: ["elytro"]
        label: "Install Elytro CLI (npm)"
---

# Elytro CLI -- Agent Skill

**Install:** `npm install -g @elytro/cli` (Node >= 24)

**Command reference and consent list:** [references/commands.md](references/commands.md)

All CLI commands return structured JSON. On error, read `error.message` and `error.data.hint` for what went wrong, and `suggestion` for what to do next. Follow those fields rather than guessing.

---

## Startup: auto-update (run every time before any other command)

Before doing anything else, the agent MUST perform these two update checks:

### 1. Check for CLI updates

```bash
elytro update check
```

If the output indicates an update is available, run:

```bash
elytro update apply
```

Report the result to the user (e.g. "Elytro CLI updated from v0.7.3 to v0.8.0").

### 2. Auto-update this skill file

Fetch the latest version of this skill from the upstream repository and overwrite the local copy:

The agent should determine the absolute path of this SKILL.md file at runtime, then download and overwrite it:

```bash
curl -fsSL https://raw.githubusercontent.com/Elytro-eth/skills/main/elytro/SKILL.md -o "<path-to-this-SKILL.md>"
```

If the download succeeds and the content differs from the current file, inform the user: "Elytro skill updated to the latest version." Then re-read the updated SKILL.md to pick up any new instructions.

If the download fails (network error, 404, etc.), continue silently — do not block the user's request.

---

## Quick start

```bash
elytro init
elytro account create --chain 11155420 --alias agent-primary
elytro account activate agent-primary
```

Recommended security setup after activation:

```bash
elytro security email bind user@example.com
elytro security spending-limit 100
elytro security status
```

## Daily use

```bash
elytro query chain
elytro query balance
```

Always simulate before sending, with the same account and `--tx` arguments:

```bash
elytro tx simulate agent-primary --tx "to:0xRecipient,value:0.1"
# show the preview to the user, wait for explicit approval
elytro tx send agent-primary --tx "to:0xRecipient,value:0.1"
```

For batch calls, repeat `--tx` in the same order for both `simulate` and `send`.

## OTP flow

Some commands pause for email verification and return an `otpPending` object. Only the user should provide the code. The agent runs `elytro otp submit <id> <6-digit-code>` on their behalf -- do not ask the user to run CLI commands for OTP. Use `elytro otp list` to see pending verifications.

## x402 payments (beta)

> Beta feature. Ask user's permission before proceeding with any paid request.

### Service discovery

Browse verified x402-compatible services before making paid requests:

```bash
elytro services                   # list all available services
elytro services <id>              # show endpoints, pricing, and example commands
```

When the user asks "what paid APIs are available" or wants to find a service, start here. The detail view includes ready-to-use `elytro request` examples per endpoint.

### Paid request workflow

1. **Discover** (if the user doesn't already have a URL): `elytro services` to browse, `elytro services <id>` for endpoint details.
2. **Preview**: `elytro request --dry-run <url>` to show the price. Always do this before paying.
3. **Set up delegation** (only if dry-run shows ERC-7710): check `delegation list` for a match. If none, guide user through `delegation add` with the server-provided parameters.
4. **Pay** (after explicit user approval): `elytro request <url> [--method POST --json '...']`.
5. **Handle failure**: if payment fails with "expired", suggest `delegation renew` or `delegation sync --prune`.

EIP-3009 (USDC) requires no delegation setup; Elytro auto-signs.

### Delegation lifecycle

```bash
# Store
elytro delegation add \
  --manager 0xDelegationManager --token 0xUSDC \
  --payee 0xMerchant --amount 1000000 \
  --permission 0xabc123... \
  --verify          # optional: simulate on-chain before storing

# Verify
elytro delegation verify <id>
elytro delegation sync --prune          # batch verify, remove expired

# Renew
elytro delegation renew <id> --expires-at 2026-04-01T00:00:00Z --permission 0xnew... --remove-old

# Revoke
elytro delegation revoke <id> --calldata 0x...   # on-chain + local
elytro delegation remove <id>                     # local only
```

Other management: `delegation list`, `delegation show <id>`.

Full workflow and troubleshooting: [docs/x402.md](docs/x402.md)

## Social recovery

Social recovery lets users designate guardians who can collectively restore wallet access. The CLI handles guardian management, backup, and recovery initiation. Guardian signing and on-chain execution happen in the external Recovery App at `https://recovery.elytro.com/`.

```bash
# Set guardians (on-chain transaction, requires user approval)
elytro recovery contacts set 0xAlice,0xBob,0xCarol --threshold 2
# Options: --label "0xAlice=Alice,0xBob=Bob"  --privacy  --sponsor

# Query / clear guardians
elytro recovery contacts list
elytro recovery contacts clear

# Backup and restore guardian info offline
elytro recovery backup export --output guardians.json
elytro recovery backup import guardians.json

# Initiate recovery (--chain is required)
elytro recovery initiate 0xWalletToRecover --chain 11155420
# Returns a recoveryUrl -- tell the user to share it with guardians

# Check recovery progress
elytro recovery status
```

When `recovery initiate` succeeds, present the `recoveryUrl` prominently and tell the user to share it with their guardians so they can approve in the Recovery App.

---

## Approval-required commands

Get explicit user confirmation before running any command listed under "Agent: user approval before running" in [references/commands.md](references/commands.md). This includes all money movement, security changes, recovery writes, delegation revocation, and OTP submission.

---

## How to explain results

Do not show raw JSON unless the user asks. Translate CLI output faithfully: preserve exact identifiers (alias, address, chain, tx hash, userOp hash, OTP id), include all warnings, and copy any next-step commands exactly. Never claim a transaction is confirmed unless the CLI says so.

Use these output shapes:

**Success:** `Done: <what changed>.` Optionally: `Next: <most useful next step>.`

**Query/status:** `Status: <plain-language summary>.` Then one short line with the most relevant facts.

**Transaction preview:**
`Preview: <transaction type>.`
`Cost: <estimated cost>. Sponsored: <yes/no>.`
`Warnings: <every warning, or "none">.`
`Please confirm if you want me to send it.`

**Transaction sent:** `Done: transaction confirmed for <account>.` with `Tx: <hash>` and `Explorer: <url>` if present. If only submitted (not confirmed): use `UserOp: <hash>` instead.

**OTP pending:**
`Action needed: email verification is required to continue.`
`Code sent to: <maskedEmail>.`
`Please send me the 6-digit code and I'll complete it for you.`

**Error:** `Couldn't complete: <reason from error.message>.` `Try: <hint from error.data.hint or suggestion>.`

**Lists:** `Found <n> item(s).` Then one short line per item with the most relevant fields.

---

## Common commands

```bash
elytro account list
elytro account info agent-primary
elytro account switch agent-primary
elytro query tx <hash>
elytro security status
elytro recovery contacts list
elytro recovery status
elytro config show
elytro update check
```
