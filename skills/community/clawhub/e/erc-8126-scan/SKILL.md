---
name: erc-8126-scan
description: Look up ERC-8004 agents in the on-chain identity index and read their Cybercentry verification results before trusting them
---

# ERC-8126 Scan

## Description

A searchable index of every agent minted in the ERC-8004 Identity Registry —
378,000+ and growing — each carrying Cybercentry verification results across
five dimensions: token contract, staking contract source, media provenance, web
application, and wallet sanctions screening.

Use this to check another agent before interacting with it: who registered it,
whether anything about it has been verified, and what was found.

The verification interface these results implement is specified in
[ERC-8126: AI Agent Verification](https://eips.ethereum.org/EIPS/eip-8126)
(Final), co-authored by the maintainers. The agents themselves are registered
under [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004),
whose on-chain Identity Registry is the source this index syncs from.

This server serves results already computed and stored. It does not run
verifications and cannot mint, write on-chain, or spend credits. All four tools
are read-only.

**Privacy notice:** queries name agents, wallets and UUIDs already public on
chain. No private data is submitted.

**Payment notice:** tools cost USDC per call over x402 — $0.001 for
`search_agents` and `get_agent`, $0.002 for `get_agent_activity`, $0.05 for
`get_agent_report`. An `erc8126_` API key is the alternative, drawing on a plan
quota instead. Listing the tools is free either way.

## Instructions

The server is remote, so there is nothing to install:

- URL: `https://erc8126scan.ai/api/mcp`
- Transport: streamable-http
- Registry name: `uk.co.cybercentry/erc-8126-scan`

In OpenClaw: `openclaw mcp add erc-8126-scan --url https://erc8126scan.ai/api/mcp --transport streamable-http`.
In Claude: Settings, Connectors, Add custom connector, paste the URL. Other MCP
clients: add a remote server at the same URL.

Payment is per call in USDC over x402, on Base or Solana — no account and no key
needed. Clients that speak x402 handle this automatically: an unpaid call comes
back as a JSON-RPC error with code 402 carrying the price and requirements, and
the client pays and retries. Alternatively pass `Authorization: Bearer
erc8126_...` to draw on a subscription quota instead; keys come from
https://erc8126scan.ai/my-api-keys.

### Before any paid call

These are cheap, but they are not free. Prefer one precise call to speculative
browsing: look an agent up by `wallet` or `id` through `search_agents` rather
than paging the index. `get_agent_report` at $0.05 is the only one worth
confirming with the user first, and it only returns agents they own.

### Always try the free tools first

Neither takes payment and neither needs a wallet or key.

- `list_services`: the live catalogue with current prices, the five verification
  dimensions, and how to read the risk fields. This is authoritative; the list
  below is a snapshot of it.
- `get_index_stats`: how many agents are indexed, so you can judge whether the
  index is likely to know about the agent in question before paying to look it
  up.

If the user's question can be answered from either, answer it from there and do
not pay for anything.

### The paid tools

- `search_agents` — filter by `chain`, `min_score`/`max_score`, `verified`,
  with `sort`, `order`, `page` and `limit`. Pass `wallet` or `id` to look up a
  single agent directly. Start here when you have an address rather than a UUID.
- `get_agent` — full detail for one agent by UUID.
- `get_agent_activity` — on-chain activity and liveness for one agent.
- `get_agent_report` — the full assessment, with per-dimension findings and
  evidence. Only for agents owned by the wallet bound to your key; anything else
  returns `FORBIDDEN_NOT_OWNER`. Use `get_agent` for public scores on any agent.

### Reading the result — the part most often got wrong

**Judge an agent by `risk_level`, never by `overall_risk_score` alone.**

Scoring presumes risk. A check that applies to an agent but has not been
verified counts as 100. An agent nobody has paid to assess therefore scores
identically to one assessed and found dangerous, and most of the index has never
been assessed.

- `not_verified` — nobody has checked this agent yet. This is **not** a finding
  against it. Do not describe such an agent as high risk, critical, dangerous or
  suspicious. Say it is unverified.
- `not_assessed` — no score recorded.
- `low`, `moderate`, `elevated`, `high` — verified, scoring in that band.
- `critical` — verified and genuinely high risk. Only this value, and `high`,
  justify warning the user about the agent itself.

The per-dimension booleans (`etv_verified`, `mcv_verified`, `scv_verified`,
`wav_verified`, `wv_verified`) show which checks actually ran. An agent may have
passed several and still read as unverified overall, because overall
verification currently keys on wallet verification.

### Reporting back

State plainly which checks have run and which have not. "Wallet screening passed;
nothing else has been verified" is an accurate and useful answer. "Risk score
100, critical" is not, when the score is 100 because nobody has looked.

If the user is deciding whether to trust an agent and nothing has been verified,
say so and let them decide whether to commission verification, rather than
presenting absence of evidence as evidence of harm.
