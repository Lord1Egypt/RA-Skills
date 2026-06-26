---
name: cdp-wallet
description: Send USDC on Base, read balances, and pay x402-protected resources using a Coinbase CDP server wallet (v2). Use when the operator needs the agent to make USDC payments, donations, or x402 settlements on Base without managing private keys directly. Wraps the official @coinbase/cdp-sdk into five CLI subcommands — address, balance, send-usdc, history, pay-x402 — that an agent can invoke directly. Wallet keys live in Coinbase's TEE infrastructure and are addressed by name, so the same wallet persists across container restarts. The pay-x402 subcommand handles the full x402 protocol negotiation (HTTP 402 → EIP-712-signed authorization → resubmit) using the same wallet.
version: 0.2.2
license: MIT-0
metadata:
  author: Ales375
  source: "https://github.com/Ales375/openclaw-cdp-wallet-skill"
  openclaw:
    homepage: "https://github.com/Ales375/openclaw-cdp-wallet-skill"
    requires:
      bins:
        - node
        - npm
      env:
        - CDP_API_KEY_ID
        - CDP_API_KEY_SECRET
        - CDP_WALLET_SECRET
    primaryEnv: CDP_WALLET_SECRET
    env:
      - name: CDP_API_KEY_ID
        description: "Coinbase CDP API key ID for server wallet access."
        required: true
        sensitive: true
      - name: CDP_API_KEY_SECRET
        description: "Coinbase CDP API key secret paired with CDP_API_KEY_ID."
        required: true
        sensitive: true
      - name: CDP_WALLET_SECRET
        description: "Coinbase CDP wallet secret used to authorize signing operations."
        required: true
        sensitive: true
      - name: CDP_NETWORK
        description: "Target EVM network for address, balance, send-usdc, and history. Defaults to base."
        required: false
      - name: CDP_ACCOUNT_NAME
        description: "Human-readable CDP account name. Reusing the same name resolves to the same wallet."
        required: false
      - name: BASE_RPC_URL
        description: "Optional override for the Base RPC URL used for on-chain reads and receipt polling."
        required: false
compatibility: Requires Node.js 22+, an internet connection, and three CDP credentials (CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET) set in the environment.
---

# cdp-wallet

A small wrapper around the [Coinbase CDP server wallet v2 SDK](https://docs.cdp.coinbase.com/server-wallets/v2/introduction/welcome) that exposes the operations an autonomous agent actually needs: get an address, check a balance, send USDC, look at transfer history, and pay x402-protected resources. Nothing else.

The wallet is a CDP server wallet — keys are generated and held inside AWS Nitro Enclaves on Coinbase's infrastructure, never on the operator's machine, and signing happens by API call against those held keys. The wallet is identified by a human-readable name (`openclaw-default` by default), not a seed phrase, so a fresh container with the same env vars resolves to the same wallet on first call. This is the right shape for unattended scheduled agents on Railway, Fly, Hetzner, etc.

## When to use

- The agent needs to send USDC on Base (donation, peer-to-peer payment).
- The agent needs to pay an x402-protected resource (gated APIs, paid evidence access, agentic-market services).
- The agent needs to know how much USDC or ETH it has before making a decision.
- The agent needs to inspect recent USDC activity on its wallet (audit, idempotency check).

## When not to use

- The agent needs to send a token other than USDC. This skill is intentionally USDC-only; the underlying SDK supports more, but the surface here is deliberately small. Wrap the SDK directly if you need swaps, ERC-20 transfers of other tokens, smart accounts, or paymaster/gasless flows.
- The agent runs on a single trusted machine and the operator wants self-custody. CDP server wallets put trust in Coinbase's TEEs. If that trust assumption is wrong for your use case, use a self-custodial path (viem EOA, Bankr, etc.) instead.
- Solana. Base only.

## Setup

### 1. Get CDP credentials

Sign in at [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com), create a CDP API key, and generate a Wallet Secret. You'll have three values:

- `CDP_API_KEY_ID`
- `CDP_API_KEY_SECRET`
- `CDP_WALLET_SECRET`

The Wallet Secret is the credential that authorizes signing operations against the keys held in CDP's TEEs. Without it, the agent can read but cannot move funds.

### 2. Install

```sh
git clone https://github.com/Ales375/openclaw-cdp-wallet-skill.git
cd openclaw-cdp-wallet-skill
npm install
```

For OpenClaw, point the skill loader at this directory or symlink `~/.openclaw/skills/cdp-wallet → /path/to/openclaw-cdp-wallet-skill`. For Hermes, place under `~/.hermes/skills/cdp-wallet`. For Claude Code or any other agentskills.io-compatible runtime, drop into the configured skills path.

### 3. Configure

Create a `.env` based on `.env.example`:

```
CDP_API_KEY_ID=...
CDP_API_KEY_SECRET=...
CDP_WALLET_SECRET=...
CDP_NETWORK=base                 # or base-sepolia for testing
CDP_ACCOUNT_NAME=openclaw-default # any name; same name → same wallet across runs
```

For Railway / Fly / Hetzner: set the same variables as service env, no `.env` needed.

### 4. First run — get the wallet address

```sh
npm run address
```

Output:

```json
{"ok":true,"address":"0x...","network":"base","account_name":"openclaw-default"}
```

Same call on a fresh container with the same env vars returns the same address. The wallet is created on first call and looked up on every call after that.

### 5. Fund the wallet

Send USDC on Base (and a small amount of ETH for gas, or use gasless paths externally) to the printed address. The minimum useful balance depends on the agent's purpose; for donations of $5 USDC at a time, fund $50–100 USDC plus $1 of ETH.

For testnet (`CDP_NETWORK=base-sepolia`), the SDK exposes faucet methods — extend this skill if needed; this minimal version doesn't include a faucet command.

## How the agent invokes it

Every subcommand prints a single JSON line to stdout and exits 0 on success or 1 on error. The agent should parse the JSON and act on the `ok` field.

### `address`

```sh
node src/index.js address
```

Prints the wallet's EVM address. Useful before donating so the agent can register itself with services that require a `wallet_address`.

### `balance`

```sh
node src/index.js balance
```

Prints ETH and USDC balances:

```json
{
  "ok": true,
  "address": "0x...",
  "network": "base",
  "eth": "0.001234",
  "usdc": "42.500000",
  "raw": { "eth_wei": "1234000000000000", "usdc_atoms": "42500000" }
}
```

Always check balance before sending. The agent's planning logic should treat the `usdc` string as the spendable amount in human units.

### `send-usdc <to> <amount>`

```sh
node src/index.js send-usdc 0xRecipientAddress 5.00
```

Sends 5 USDC on Base to `0xRecipientAddress`. Waits for one confirmation by default.

Success:

```json
{
  "ok": true,
  "tx_hash": "0xabc...",
  "status": "confirmed",
  "explorer": "https://basescan.org/tx/0xabc...",
  "from": "0x...",
  "to": "0xRecipientAddress",
  "amount_usdc": "5.00",
  "network": "base"
}
```

Submitted but confirmation timed out (rare; means the chain is congested or RPC is slow):

```json
{ "ok": true, "tx_hash": "0xabc...", "status": "submitted_unconfirmed", ... }
```

In this case the transaction is on-chain but the CLI gave up waiting for the receipt. The agent should poll the explorer or call `history` after a short delay to confirm.

Failures (validation, CDP API error, on-chain revert):

```json
{ "ok": false, "error": "...", "phase": "submit" }
```

### `history --limit <N>`

```sh
node src/index.js history --limit 10
```

Returns the last N USDC Transfer events involving this wallet (in or out), looking back ~24h on Base by default. Use `--lookback <blocks>` to extend. Pure on-chain read against Base RPC; doesn't depend on any CDP-side history API.

```json
{
  "ok": true,
  "address": "0x...",
  "count": 3,
  "transfers": [
    {
      "direction": "out",
      "from": "0x...",
      "to": "0xRecipient",
      "amount_usdc": "5.000000",
      "block_number": "12345678",
      "tx_hash": "0xabc...",
      "explorer": "https://basescan.org/tx/0xabc..."
    }
  ]
}
```

### `pay-x402 <url>`

```sh
node src/index.js pay-x402 https://api.example.com/protected
node src/index.js pay-x402 https://api.example.com/protected -H "Authorization: Bearer abc123"
node src/index.js pay-x402 https://api.example.com/protected -X POST -d '{"k":"v"}' -H "Content-Type: application/json"
```

Calls an x402-protected URL. The x402 protocol is an HTTP-native payment scheme: the server returns a 402 with payment requirements, the client signs an EIP-712 authorization, the server's facilitator settles on-chain, the resource is returned. From the agent's perspective, this is one call — the negotiate-sign-resubmit dance happens transparently.

Options:

- `-X, --method <method>` — HTTP method, default `GET`.
- `-H, --header <name: value>` — request header. Repeat the flag for multiple headers.
- `-d, --body <body>` — request body string. Only valid with non-GET methods.

Success:

```json
{
  "ok": true,
  "status": 200,
  "content_type": "application/json",
  "body": { "...": "the resource" },
  "body_truncated": false,
  "settlement": {
    "transaction": "0xabc...",
    "amount": "10000",
    "network": "eip155:8453",
    "...": "facilitator-defined fields"
  },
  "settled_amount_usdc": 0.01
}
```

The `settlement` object is the decoded `PAYMENT-RESPONSE` header from the server. `settled_amount_usdc` is a convenience conversion assuming USDC (6 decimals); ignore it if the resource server settled in a different asset.

Body handling:

- If `Content-Type` is `application/json`, the body is parsed and embedded as a JSON object/array.
- Otherwise the body is returned as a string.
- If the body exceeds 200,000 characters, it's returned as `{_truncated: true, _length, preview}` and `body_truncated: true`. Increase the limit by editing the skill source if needed.

Failure (server returned non-2xx, or request failed):

```json
{
  "ok": false,
  "error": "x402 endpoint returned 401 Unauthorized",
  "status": 401,
  "content_type": "application/json",
  "body": { "error": "..." },
  "body_truncated": false,
  "settlement": null,
  "settled_amount_usdc": null
}
```

Network choice. The x402 protocol is network-aware — the resource server tells the client which network to pay on (e.g., `eip155:8453` for Base mainnet, `eip155:84532` for Base Sepolia). `pay-x402` honours whatever the server requests. The `CDP_NETWORK` env var does NOT constrain `pay-x402`; it only affects `address`, `balance`, `send-usdc`, and `history`. If the operator wants to restrict which networks the agent will pay on, do that at the prompt or persona level, not in the skill.

The signer is the same CDP wallet used by `send-usdc`. The agent's address as `wallet_address` (in zooidfund's case) and the address that signs the x402 payment authorization are the same address — no mismatch risk.



## Failure modes the agent should know about

- **Missing env vars** → `ok: false, error: "Missing required env: ..."`. The agent has no recovery path for this; the operator must fix the deployment.
- **Invalid recipient address** → `ok: false`. The agent should validate addresses before invoking `send-usdc`.
- **Insufficient USDC balance** → CDP returns an error from `submit` phase. The agent should call `balance` first.
- **Insufficient ETH for gas** → same. The wallet needs a small ETH balance unless the operator has wired a paymaster.
- **OFAC-screened recipient** → CDP refuses to submit. Skip that recipient rather than retry.
- **`status: "submitted_unconfirmed"`** → tx is on-chain, the CLI just didn't see the receipt within the timeout. Don't re-send; poll `history` or the explorer.
- **CDP API outage** → transient, retry with backoff.
- **`pay-x402` returns ok:false with a 402 status** → the x402 client could not satisfy the server's payment requirements (e.g., server requested an unsupported network/scheme, or the wallet lacked funds). Inspect the response body for the server's `accepts` array — that lists what the server would accept. If the agent's wallet can't satisfy any option, give up rather than retry.
- **`pay-x402` returns ok:false with phase: "request"** → request never completed (network failure, DNS, TLS, malformed URL not caught by upfront validation). Retry once with backoff before giving up.
- **`pay-x402` succeeds but `settlement` is null** → the resource was returned without a `PAYMENT-RESPONSE` header. This usually means the resource was free (server didn't gate it after all) or the server doesn't echo settlement details on this path. Treat as success.

## Why CDP server wallets and not other paths

CDP server wallets v2 was chosen because: keys never reach the operator's filesystem (eliminates a whole class of leak); wallet creation is programmatic and idempotent (no interactive OTP, no seed phrase to lose); the SDK is first-party and current; and the policy engine can layer spending caps on top of this skill at the CDP-account level if the operator wants infrastructure-enforced limits in addition to whatever the agent enforces in its own logic.

The skill deliberately does not enforce per-transaction limits, daily caps, or whitelists in code. Those belong either in the CDP policy engine (for hard infrastructure-level guarantees that survive a compromised agent) or in the agent's own reasoning layer (for soft limits that depend on context). Putting them in the skill code creates the worst of both worlds — bypassable from the agent if it controls the env, but invisible to the operator if it doesn't.

## Security notes

- Use a dedicated OpenClaw agent or workspace for this skill. Do not share one funded wallet across unrelated agents or tenants.
- The Wallet Secret is the most sensitive credential; protect it with the same care as a private key. Anyone with all three env vars can move the wallet's funds.
- This skill prints the wallet address but never the keys (the SDK doesn't expose them).
- Output JSON includes addresses, amounts, and tx hashes only — no secrets are logged.
- If you suspect credential compromise, rotate the Wallet Secret in the CDP portal immediately. Existing transactions can't be reversed but new ones become impossible.
