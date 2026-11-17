# CreditClaw — Virtual Cards for AI Agents

Give your AI agent spending power you control. CreditClaw issues **Virtual Cards** from your own Visa/Mastercard — each with its own spending limit, expiry date, and agent link. Your agent mints fresh one-time card numbers right before each purchase and fills the merchant's payment form; limits are enforced at the card network, and you can freeze or revoke a card at any time.

- **Website:** https://creditclaw.com
- **Skill (agent-facing):** https://creditclaw.com/SKILL.md
- **API base:** `https://creditclaw.com/api/v1`

## Installation

**OpenClaw / ClawHub:**

```bash
clawhub install creditclaw
```

**skills.sh (Claude Code, Cursor, Codex, Copilot, and 20+ agents):**

```bash
npx skills add jononovo/claw-skill
```

## Setup

1. Your agent registers itself via the API (see `SKILL.md`) and receives a `CREDITCLAW_API_KEY`.
2. You sign in at [creditclaw.com](https://creditclaw.com), add your card, and create a Virtual Card linked to your agent — with the spending limit you choose.
3. That's it. Your agent can now pay online within your limits.

## Required environment

| Variable | Description |
|---|---|
| `CREDITCLAW_API_KEY` | Issued to your agent at registration. Cannot be retrieved again — store it securely. |

## Usage

Once installed, your agent uses the skill automatically when you ask it to buy something:

> "Order this book from acmebooks.com for me."

The agent lists its linked cards, mints fresh merchant-locked card numbers, fills the checkout form, and stops for you on any CAPTCHA, 3-D Secure, or OTP challenge. Every credential issuance is logged to your dashboard.

## Safety model

- Card numbers are one-time and merchant-locked — minted per purchase, discarded after use.
- Spending limits are enforced at the card network, not by agent goodwill.
- You can freeze, unfreeze, or revoke any Virtual Card instantly from your dashboard.
- The agent's API key only works against `creditclaw.com`.

## License

MIT
