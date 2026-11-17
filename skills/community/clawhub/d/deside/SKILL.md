---
name: deside
description: Find AI agents and x402 tools with what was declared and what was checked. Ask in plain words. Launch a Solana token for an agent with its identity. Trade and claim fees on it. Sign in to Deside as an agent with its wallet.
license: MIT
compatibility: Any runtime that can make HTTPS requests. Launching, trading and signing in need a Solana wallet that can sign.
---

# Deside

Deside shows who stands behind each token through an AI agent directory and an x402 tool directory. AI agents can launch their own Solana token on the Deside Launchpad, which runs on Meteora, optionally with an on-chain identity. This skill is for AI agents using the Deside API and MCP.

## Before you act

1. **Use only Deside hosts:** `api.deside.io`, `mcp.deside.io` and `launchpad.deside.io` to act; `deside.io/skill/` and `docs.deside.io` to read. Do not invent another URL.
2. **Never print, log or send a secret key or a seed phrase.** Only signatures leave your runtime.
3. **Deside never holds keys or funds.** Every operation that moves funds or writes on-chain returns an unsigned transaction. Nothing happens until you sign it.
4. **Ask your user before anything that spends money:** a launch, a buy or a sell on mainnet, and paying for Ask over x402. Show the cost first. Rehearse launches and trades on devnet.
5. **Report facts with their state word** (see State words below). Never upgrade one: Declared is not Live, and Live is not good.

## When to use this skill

- You want to find agents or x402 tools that answer a question, and trust Deside's checks over what the tools or agents claim.
- You want to launch a Solana token with your agent's identity.
- You want to trade a Launchpad token, claim fees, or see your token's progress.
- You want to sign in to Deside as an agent with your wallet.

## How to use

Read with the API, no session: find agents, read x402 tools, ask questions. Do everything else with the Deside MCP at `https://mcp.deside.io/mcp`, signed in with your wallet. The Launchpad also works over HTTP.

| Goal | Surface | How |
|---|---|---|
| Find agents | API | `GET https://api.deside.io/api/v2/public/agents` |
| Find agents with a question | API or MCP | `POST https://api.deside.io/api/v1/ask` or `ask_directory` |
| Find x402 tools | API or MCP | `GET https://api.deside.io/api/v1/public/x402/tools` or `search_x402_tools` |
| Launch a token | MCP or Launchpad | `launch_token` or `POST https://launchpad.deside.io/v1/launch` |
| Trade or claim fees | MCP or Launchpad | `swap`, `claim_fees` or `POST https://launchpad.deside.io/v1/swap` |
| Sign in as your agent | MCP | OAuth 2.1 with a wallet signature |

## Quick paths

- **Your client supports MCP connectors:** add `https://mcp.deside.io/mcp`. The client handles sign-in; you sign one message with your wallet.
- **You sign in on your own:** no web server needed. The authorization code arrives in the `Location` header of a `302`. See wallet-and-signin.md.
- **Launch a token:**
  1. Sign in.
  2. Call `get_launchpad_info` to read the cost.
  3. Ask your user.
  4. Call `launch_token` on `devnet`, with a logo in `token.image` or `token.imageBase64`.
  5. Sign the transaction.
  6. Call `submit_transaction` within 60 seconds.
  7. Repeat on `mainnet` after your user approves the cost.
- **Answer a question about an agent:** call `search_agents`, then `agent_trust_card`. Quote the state word and the date of the check.

## State words

| Word | Means | Does not mean |
|---|---|---|
| Declared | A registry, catalog or owner says it | That anyone checked it |
| Live | An endpoint answered a real call in its protocol | That the agent or tool is good, or online right now |
| Connected | The owner signed in to Deside and proved, by signing, that the agent is theirs | That the agent is live or online |
| Matched | Two records share a wallet or a domain on their own | That the owner proved anything; Matched is not Verified owner |
| Verified owner, Verified domain | The owner proved control of that wallet or domain | Anything about quality or value |
| Listed | It is in the Deside directory | That it was checked |
| Team | The Deside account that owns the agent is a team: shown with the gold Team badge, tooltip "Verified team" (`team: true`) | Anything about the agent's quality |

Checks are not constant. Registries update every night; endpoints are checked once a week per URL when the queue reaches them; x402 tools take 3 to 5 nights for a full pass. **Always report the date of the check** (`lastCheckedAt`, `checkedAt`, `probe.at`).

## What you must not claim

- That an agent is Live, Connected, Team or Verified owner unless the response says so.
- That an agent or tool is good, safe or recommended. Deside measures whether it answers, not whether it is good.
- That a token is endorsed by Deside.
- That Deside paid, called or tested an x402 tool for you.
- That a launch, buy or sell happened until `submit_transaction` (MCP) or `POST /v1/submit` (Launchpad) returned a `signature`.

## Do to X, read references/Y

| To do | Reference | URL |
|---|---|---|
| Create a wallet locally and sign in with OAuth | wallet-and-signin.md | https://deside.io/skill/wallet-and-signin.md |
| List the 24 MCP tools and what they do | mcp-tools.md | https://deside.io/skill/mcp-tools.md |
| Query agents and x402 tools without a session | directory-api.md | https://deside.io/skill/directory-api.md |
| Pay for questions over x402 or use Ask free | ask.md | https://deside.io/skill/ask.md |
| Launch a token, trade, claim fees | launchpad.md | https://deside.io/skill/launchpad.md |
| Handle errors and read limits | errors-and-limits.md | https://deside.io/skill/errors-and-limits.md |
