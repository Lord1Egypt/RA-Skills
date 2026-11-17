---
name: agentgates-cli
description: "Give your agent an account in one command: twelve words that sign every call, hold a prepaid USDC balance and lock the vault, then compute, inference, phone, email and calls from the terminal or as MCP tools."
---

# Agentgates CLI: an account for your agent in one command

Twelve words are the account. They sign every call, hold the prepaid USDC
balance and lock the vault. No signup, no session, nothing to refresh.

## Start

```bash
npm i -g @agentgates/cli
agentgates init               # mints the words once and prints them, with what to tell your human
agentgates browser balance    # the balance, and the address that tops it up
```

`agentgates init --seed "<twelve words>"` brings words a human gave you.

## What it drives

- `agentgates compute`, `agentgates inference`: machines by the hour, models by the request.
- `agentgates phone`, `agentgates call`, `agentgates email`: numbers, the AI operator, inboxes.
- `agentgates mcp install`: the same lanes as MCP tools over stdio, signed by this machine's key.
- `agentgates keys`: login keys (`agk_…`) an agent sends instead of a signature, one per agent, revocable.
- `agentgates --help` lists every command.

## Coming back

Nothing to log in: the key on this machine signs every call. A new machine
takes the words. `agentgates open` hands the session to a person's
browser; `agentgates receive` takes one back.

## Endpoints (all on https://api.agentgates.ai)

- `GET /api/account/docs`: the whole account contract.
- `GET /api/account/catalog`: products, plans and prices, machine-readable.

Every request carries `X-Wallet-Auth` (a signature over the method, the
path, a nonce and a timestamp) or `Authorization: Bearer agk_…`.

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.
