# Botwallet — Give Your AI Agent a Wallet

**Three commands. Your agent can pay, earn, and invoice — with real money.**

Botwallet is the payment CLI for AI agents. Install it, and your agent gets a real USDC wallet on Solana with human oversight, spending limits, and FROST threshold signing built in.

## Why Install This Skill?

Your agent can talk about money. With Botwallet, it can actually **move** money:

- **Create invoices** and get paid — the paylink feature lets your agent bill clients, other agents, or anyone with an email
- **Pay** other agents or merchants instantly on Solana
- **Access paid APIs** through the x402 protocol — probe prices first, pay only when ready
- **Request funds** from you when its balance is low
- **Withdraw** USDC to any Solana address

All within guard rails you control: per-transaction limits, daily caps, merchant allowlists, and approval gates.

## Quick Start

```bash
npm install -g @botwallet/agent-cli
botwallet register --name "My Agent Wallet" --owner you@email.com
```

That's it. Your agent has a wallet. You claim it through the [Botwallet Dashboard](https://app.botwallet.co), set spending limits, and fund it.

## What Makes Botwallet Different

- **CLI-first** — designed for agents with shell access, not humans clicking buttons
- **FROST 2-of-2 threshold signing** — the full private key never exists anywhere. Agent holds one share, server holds the other. Neither can sign alone
- **Human oversight built in** — you set the rules, your agent operates within them
- **Real money, not tokens** — USDC on Solana. $10.00 means $10.00
- **Open source** — Apache 2.0. Read every line of code

## How Payments Work

Every transaction follows a two-step pattern:

```bash
botwallet pay @merchant 10.00           # Step 1: Create intent (server checks guard rails)
botwallet pay confirm <transaction_id>  # Step 2: FROST sign & submit to Solana
```

If the payment exceeds your guard rails, it pauses and waits for your approval in the dashboard. Nothing moves without your OK.

## The Paylink Feature

The feature users love most. Your agent creates a payment link anyone can pay:

```bash
botwallet paylink create --desc "Dev services" \
  --item "API Calls, 5.00, 2" \
  --item "Setup Fee, 10.00"

botwallet paylink send <id> --to client@example.com --message "Here's your invoice"
```

Humans pay via web interface. Agents pay with `botwallet pay --paylink <id>`. Funds arrive instantly.

## Requirements

- Node.js 18+ (for `npm install -g`) or Go (for `go install`)
- Shell access (the skill runs CLI commands)
- Network access (CLI communicates with the Botwallet API at `api.botwallet.co`)

## Links

- **Website**: [botwallet.co](https://botwallet.co)
- **Dashboard**: [app.botwallet.co](https://app.botwallet.co)
- **CLI Source**: [github.com/botwallet-co/agent-cli](https://github.com/botwallet-co/agent-cli)
- **Docs**: [docs.botwallet.co](https://docs.botwallet.co)
- **npm**: [@botwallet/agent-cli](https://www.npmjs.com/package/@botwallet/agent-cli)

## License

Apache-2.0
