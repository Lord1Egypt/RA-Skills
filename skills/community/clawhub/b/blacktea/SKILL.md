---
name: blacktea
description: Spending controls for AI agents that pay online via x402. Set limits, require human approval, audit every payment.
version: 0.1.0
author: nmrtn
license: MIT
platforms: [macos, linux]
homepage: https://github.com/nmrtn/blacktea
metadata:
  openclaw:
    emoji: "🫖"
    homepage: https://github.com/nmrtn/blacktea
    requires:
      bins: [npx]
      env: [EVM_PRIVATE_KEY]
    primaryEnv: EVM_PRIVATE_KEY
    envVars:
      - name: EVM_PRIVATE_KEY
        required: true
        description: Wallet private key (0x-prefixed) used to sign x402 USDC payments on Base.
      - name: BLACKTEA_POLICY
        required: false
        description: Path to the spending-policy JSON file. Defaults to ./policy.json.
  hermes:
    tags: [Payments, Agent Safety, x402, Spending Controls]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: EVM_PRIVATE_KEY
    prompt: "Enter the wallet private key for agent payments (0x-prefixed)"
    help: "A funded Base wallet key. blacktea signs x402 USDC payments with it. Kept local, never shown to the model."
    required_for: "Signing x402 payments"
---

# blacktea: spending controls for paying agents

## When to use

Use blacktea whenever this agent might pay for something online: a paywalled
API, a premium data feed, any x402-enabled endpoint. blacktea sits between the
agent and its wallet and enforces a spending policy before any money moves. It
auto-approves small amounts, asks the human for larger ones, rejects what is
over the line, and writes an audit log of every payment.

## Setup (runs as a local MCP server)

blacktea ships as an MCP server. Register it once.

OpenClaw (`~/.openclaw/openclaw.json`, or `openclaw mcp set`):

```json
{
  "mcp": {
    "servers": {
      "blacktea": {
        "command": "npx",
        "args": ["-y", "@nmrtn/blacktea-mcp"],
        "env": {
          "EVM_PRIVATE_KEY": "0x...",
          "BLACKTEA_POLICY": "/path/to/policy.json"
        }
      }
    }
  }
}
```

Hermes:

```bash
hermes mcp add blacktea \
  --command npx \
  --args -y @nmrtn/blacktea-mcp \
  --env EVM_PRIVATE_KEY=0x... BLACKTEA_POLICY=/path/to/policy.json
```

No wallet handy? Add `BLACKTEA_RAIL=mock` (and optionally
`BLACKTEA_MOCK_AMOUNT=5`) to exercise the full policy and approval flow with no
x402 endpoint, no USDC, and no signing.

## Tools this exposes

- `pay(url, intent, max_amount?)`: attempt a paid request. Runs the policy
  first. If the policy holds it for approval, returns
  `status: "approval_required"` with an `intent_id` and the amount, and does
  NOT pay yet. If allowed, settles and returns the response data plus a receipt.
- `approve_payment(intent_id)`: settle a held payment, after the human confirms.
- `reject_payment(intent_id)`: decline a held payment. Nothing is charged.
- `audit_query(limit?)`: recent payment events from the audit log.

## Ask before spending

When `pay` returns `approval_required`, do NOT treat it as a failure. Tell the
human the amount and what it is for, in plain language, and only call
`approve_payment` after they say yes. Below the auto-approve limit it just pays.
Over the hard limit it rejects. The human stays in the loop without leaving the
chat.

## Policy

A `policy.json` governs every payment. Example:

```json
{
  "rules": [
    { "if": { "amount_lt": 1 }, "then": { "approve": true } },
    { "if": { "amount_gte": 100 }, "then": { "reject": "over_hard_limit" } }
  ],
  "default": { "approval": "callback" }
}
```

This auto-approves under 1 USDC, asks the human between 1 and 100, and rejects
over 100. The full operator set is in the policy cookbook (see Links).

## Pitfalls

- The wallet key signs real payments. Use a dedicated agent wallet funded only
  with what you are willing to let the agent spend.
- Through MCP, rely on the approve/reject tools, not a console prompt. The
  server holds the payment and asks for confirmation through the chat.

## Verification

Run with `BLACKTEA_RAIL=mock` and `BLACKTEA_MOCK_AMOUNT=5` and a policy that
auto-approves only under 1 USDC. Ask the agent to pay any URL. It should pause,
ask you to approve 5 USDC, settle only after you approve, and `audit_query`
should then show the settled payment.

## Links

- Repo: https://github.com/nmrtn/blacktea
- npm: https://www.npmjs.com/package/@nmrtn/blacktea-mcp
- Policy cookbook: https://github.com/nmrtn/blacktea/blob/main/docs/policy-cookbook.md
