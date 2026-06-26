---
name: eqvps
description: Rent and operate a no-KYC cloud VPS over MCP — pick a plan, deploy, get root SSH. Pay with crypto (USDC/USDT) or card.
version: 1.0.2
metadata:
  openclaw:
    primaryEnv: EQVPS_API_TOKEN
    envVars:
      - name: EQVPS_API_TOKEN
        required: false
        description: Existing EQVPS API token to reuse an account. If unset, the skill registers a new account and returns a token to save.
    emoji: "🖥️"
    homepage: https://eqvps.com
---

# EQVPS — rent and manage a VPS for your agent

EQVPS is a crypto-native, no-KYC hosting provider with a programmatic, agent-friendly
API and MCP server. Use this skill when the user asks to spin up, deploy, list, or
manage a virtual private server (VPS) — e.g. to host a bot, a website, a script, or any
workload that needs to run somewhere persistent.

**This is a paid third-party service.** Servers are billed from a prepaid account
balance. The user funds the balance with **crypto (USDC / USDT on Base, Ethereum or
Tron) or a card** (Apple Pay / Google Pay work at checkout). The agent must show prices
and get the user's explicit confirmation before any paid action, and must never spend
beyond the funded balance.

## Setup (one time)

EQVPS exposes a Model Context Protocol (MCP) server. Add it to your `openclaw.json`
so its tools become available, then restart the OpenClaw gateway:

```json
{
  "mcpServers": {
    "eqvps": { "url": "https://mcp.eqvps.com/mcp" }
  }
}
```

It is a Streamable HTTP MCP server; if your OpenClaw version needs an explicit
transport/type field, see the OpenClaw MCP docs. Once connected, all **16 EQVPS tools**
appear automatically:

- **Account:** `register_account`, `login`, `whoami`
- **Billing:** `get_balance`, `topup_balance`, `pay_invoice`
- **Catalog & order:** `list_plans`, `order_vps`
- **Manage:** `list_vps`, `get_vps_status`, `power_vps`, `reinstall_vps`,
  `set_hostname`, `reset_password`, `get_vps_metrics`, `cancel_service`

Each tool describes its own input fields — read them before calling.

## Workflow

1. **Account.** If `EQVPS_API_TOKEN` is set, you already have an account — go to step 3.
   Otherwise call `register_account` (email), store the returned token, and tell the
   user to save it as `EQVPS_API_TOKEN` for next time. Use `whoami` to verify a token.
2. **Funds.** Call `get_balance`. If it is too low for the chosen plan, call
   `topup_balance` — it returns a checkout link (pay with crypto or card). Tell the user
   the amount, let them complete and confirm payment, and do not proceed until the
   balance reflects it. (`pay_invoice` does the same for an existing unpaid invoice.)
3. **Plan.** Call `list_plans` and show the user the options with prices. There are two
   kinds: NAT (shared IP, SSH over a port — cheapest, good for bots/agents) and
   dedicated-IP (own IP, all ports — for sites/mail). Confirm the choice and that the
   user accepts the cost.
4. **Deploy.** Call `order_vps` with the chosen plan and OS. This draws from the balance.
5. **Access.** Call `get_vps_status` for the IP, SSH port, and root credentials once
   provisioning completes. Give these to the user and treat credentials as secret.
6. **Manage.** Use `power_vps` (start/stop/reboot), `reinstall_vps`, `set_hostname`,
   `reset_password`, `get_vps_metrics` (CPU/RAM/disk usage), `list_vps`. Use
   `cancel_service` to stop billing a server no longer needed.

## Rules

- Always show the price and get explicit user confirmation before `topup_balance`,
  `pay_invoice` and `order_vps`. Money actions are never silent.
- Never order a server the balance cannot cover.
- Treat API tokens and root credentials as secrets: show them to the user, do not log
  or post them anywhere else.
- If the user only wants information (plans, status, balance), do not place any order.
