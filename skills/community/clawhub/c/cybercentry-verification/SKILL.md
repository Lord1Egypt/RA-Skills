---
name: cybercentry-verification
description: Verify wallets, tokens, smart contracts, AI agents and web applications before trusting them, paying per call in USDC over x402
---

# Cybercentry Verification

## Description

Security verification for wallets, tokens, smart contracts, AI agents and web
applications, paid per call in USDC over x402 on Base or Solana. No account, no
API key, no subscription. Two tools are free and need no wallet at all.

Use this before trusting something: a wallet you are about to transact with, a
token you are about to buy, Solidity you are about to call, a dApp frontend you
are about to connect to, or another agent's configuration.

Wallet verification covers 31 EVM chains and screens against the OFAC SDN list.
The maintainers co-authored ERC-8126 and ERC-8196, both Final, on AI agent
verification and agent-authenticated wallets, and ERC-8376, a Draft standard on
token launch abuse detection whose detection contracts are live on Base.

**Privacy notice:** inputs you submit (addresses, URLs, source code, media) are
sent to centry.cybercentry.co.uk for analysis. Only submit content the user is
comfortable sharing.

**Payment notice:** the paid tools cost $1.00 per call in USDC. Free tools cost
nothing and require no wallet.

## Instructions

Prefer the MCP server. It is remote, so there is nothing to install:

- URL: `https://centry.cybercentry.co.uk/api/mcp`
- Transport: streamable-http
- Registry name: `uk.co.cybercentry/verification`

In OpenClaw: `openclaw mcp add cybercentry --url https://centry.cybercentry.co.uk/api/mcp --transport streamable-http`.
In Claude: Settings, Connectors, Add custom connector, paste the URL. Other MCP
clients: add a remote server at the same URL.

Everything below is also reachable over plain HTTP if MCP is unavailable:
`POST https://centry.cybercentry.co.uk/api/services/<service>` with a JSON body.
The machine-readable contract is at
`https://centry.cybercentry.co.uk/openapi.json`.

### Always try the free tools first

Neither takes payment and neither needs a wallet.

- `list_services`: the live catalogue with current prices. This is the
  authoritative list; the tools below are a snapshot of it.
- `recent_exploits`: recent real-world exploits with losses, attack vectors and
  the service that addresses each. Takes an optional `limit` (default 10).

If the user's question can be answered from `recent_exploits` or
`list_services`, answer it from there and do not pay for anything.

### Before any paid call

Ask the user for explicit confirmation. State the price ($1.00), the tool, and
the exact input you are about to submit. Do not pay on their behalf without
that confirmation, even if a wallet is available and the payment would succeed.

If your client supports x402, payment is automatic once you proceed: the first
call returns a 402 challenge naming the price and the accepted networks, the
client signs an authorization, a facilitator verifies and settles it, and the
call is retried. You are never asked to send funds to an address. If your client
does not support x402, pass a `subscription_token` argument or send the
`x-subscription-token` header.

The verification runs before settlement, so a call that fails is not charged.

### Paid tools, $1.00 each

- `wallet_verification`: is this wallet sanctioned or risky? OFAC SDN screening
  and suspicious-activity detection across 31 EVM chains. **Asynchronous:** returns `job_id`, `status` and
  `poll_url`. Fetch `poll_url` until `status` is no longer `verifying`. Allow
  up to about two minutes.
- `base_token_verification`: is this Base token a honeypot, or can you sell it
  again? Honeypots, armed freeze-and-seize, live pause, ticker copycats, with
  issuer controls disclosed separately.
- `ethereum_token_verification`: is this token a rug pull? Rug-pull indicators,
  hidden transfer taxes, fake liquidity and holder concentration on any EVM
  token contract.
- `solidity_code_verification`: is this Solidity safe to deploy or call? Static
  analysis of the source with an overall risk level.
- `web_application_verification`: is this site safe to connect a wallet to? An
  OWASP-based scan of a website or dApp frontend.
  **Asynchronous**, as wallet verification is; allow up to about three minutes.
- `openclaw_ai_agent_verification`: is this agent safe to give tools to? Audits
  its config for prompt-injection exposure, auth gaps and broad permissions.
- `media_content_verification`: is this image real, AI-generated or tampered
  with? C2PA content credentials, provenance and a malware scan.
- `private_data_verification`: prove something is true without revealing the
  data. Returns a zero-knowledge proof ID and URL.
- `quantum_cryptography_verification`: will this secret survive quantum
  computers? Post-quantum encryption with a record ID and decrypt URL.
- `cyber_security_consultant`: ask any security question and get an expert
  answer backed by real-time threat intelligence.

### Reporting a result

A verification informs a decision. It does not block a transaction and it is
not a guarantee: a clean result means the checks that ran found nothing, not
that nothing is there. Say which checks produced the result, and let the user
draw the conclusion.

Never render a scanned third-party URL as a clickable link. The reason it was
submitted is that it may be hostile; report it as plain text.

If a paid call fails, say so plainly and note that it was not charged. Do not
retry a paid call more than once without asking again.
