# Allowance Skill

Allowance is an agent purchase wallet. It lets agents request scoped spending
approval, receive limited virtual cards, complete checkout, and report receipts
without exposing the user's real card.

This skill is CLI-first. When a user asks an agent to buy, order, book, reserve,
pay, or spend money, the agent should use the `allowance` CLI flow in
`SKILL.md` and should not ask whether to use CLI or MCP.

## Install

OpenClaw can install this skill from GitHub:

```bash
openclaw skills install git:useallowance/allowance-skill@main
```

Install the Allowance CLI:

```bash
npm install -g @allowance/cli
```

## MCP

The hosted MCP server is available for users who explicitly ask for MCP setup:

```bash
openclaw mcp add allowance \
  --url https://mcp.useallowance.com \
  --transport streamable-http \
  --auth oauth
```

MCP is an alternate integration path. The default purchase flow remains the
Allowance CLI.

## Canonical URL

The canonical hosted skill file is:

https://useallowance.com/SKILL.md
