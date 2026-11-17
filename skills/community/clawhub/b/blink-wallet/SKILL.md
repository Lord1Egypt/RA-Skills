---
name: blink-wallet
description: Bitcoin Lightning wallet for agents — balances, invoices, payments, BTC/USD swaps, QR codes, price conversion, transaction history, non-custodial (Spark) accounts, and L402 auto-pay client via the Blink API. All output is JSON.
version: 3.0.5
repository: https://github.com/blinkbitcoin/blink-skills
metadata:
  oa:
    project: blink
    identifier: blink-wallet
    version: '3.0.5'
    expires_at_unix: 1798761600
    capabilities:
      - http:outbound
      - filesystem:read
      - filesystem:write
  openclaw:
    requires:
      # No env var is required skill-wide: `resolve-receiver` and
      # `create-invoice-lnaddress` work with no credentials at all. Each command
      # states its own requirement — BLINK_API_KEY for custodial operations,
      # SPARK_MNEMONIC + BREEZ_API_KEY for the seed-gated spark-* commands.
      bins: [node]
    optionalEnv:
      [
        BLINK_API_KEY,
        BLINK_API_URL,
        BLINK_WS_URL,
        BLINK_L402_ROOT_KEY,
        BLINK_BUDGET_HOURLY_SATS,
        BLINK_BUDGET_DAILY_SATS,
        BLINK_L402_ALLOWED_DOMAINS,
        SPARK_MNEMONIC,
        BREEZ_API_KEY,
        SPARK_NETWORK,
        SPARK_LNURL_DOMAIN,
      ]
    primaryEnv: BLINK_API_KEY
    emoji: '⚡'
    homepage: 'https://github.com/blinkbitcoin/blink-skills'
    security:
      secrets: ['BLINK_API_KEY', 'SPARK_MNEMONIC', 'BREEZ_API_KEY']
      network: "outbound HTTPS to api.blink.sv (or BLINK_API_URL override); outbound WSS to ws.blink.sv for subscriptions; outbound HTTPS to blink.sv for LNURL-pay receive (allowlisted, every redirect re-checked); outbound HTTPS to Breez/Spark infrastructure for spark-* commands and l402-pay --spark (the SDK connect also contacts blink.sv, the pinned Lightning-address domain, to recover the wallet's registered address — even on a dry run); spark-send/spark-fee-probe with a Lightning Address or LNURL destination also contact the recipient's address/callback hosts during SDK parse/prepare (before a budget rejection)"
      filesystem: 'reads nothing outside ~/.blink; writes temporary QR PNGs to /tmp; writes L402 token cache to ~/.blink/l402-tokens.json; writes budget config to ~/.blink/budget.json and spending log to ~/.blink/spending-log.json; writes Breez Spark SDK wallet state to ~/.blink/spark/<network>-<hash> when a spark-* command or l402-pay --spark is used'
      persistence: 'L402 token cache at ~/.blink/l402-tokens.json; budget config at ~/.blink/budget.json; spending log at ~/.blink/spending-log.json (auto-pruned, 25h retention); Spark SDK local wallet state at ~/.blink/spark/<network>-<hash>, the directory name being a non-reversible sha256 prefix of the seed'
      notes: 'Zero required npm runtime dependencies; the custodial commands use Node.js built-ins only. Two OPTIONAL, lazy-loaded dependencies exist solely for the non-custodial spark-* commands and l402-pay --spark: @breeztech/breez-sdk-spark (Node 22.4+, requires a native better-sqlite3 build) and bip39 (seed checksum validation). Nothing is loaded unless a spark-* command or l402-pay --spark is invoked. SPARK_MNEMONIC grants full spend authority over a self-custodial wallet: it is read from the environment only, never from files, and is never logged or written in readable form. BLINK_API_KEY is likewise read from the environment only; shell rc files are never read.'
---

# Blink Skill

Bitcoin Lightning wallet operations via the Blink API. Enables agents to check balances, receive payments via invoices, send payments over Lightning, track transactions, monitor prices, and automatically pay for L402-gated web services.

## What is Blink?

Blink is a Bitcoin Lightning wallet with a GraphQL API. Accounts are either
**custodial** (Blink holds the keys; this is the default and what most commands
target) or **non-custodial (Spark)** (the user holds a seed). See
`references/non-custodial.md` for the non-custodial commands
(`resolve-receiver`, `create-invoice-lnaddress`, and the seed-gated `spark-*`
commands). Key concepts:

- **API Key** — authentication token (format: `blink_...`) with scoped permissions (Read, Receive, Write)
- **BTC Wallet** — balance denominated in satoshis
- **USD Wallet** — balance denominated in cents (stablecoin pegged to USD)
- **Lightning Invoice** — BOLT-11 payment request string (`lnbc...`) used to receive payments
- **Lightning Address** — human-readable address (`user@domain`) for sending payments without an invoice
- **LNURL** — protocol for interacting with Lightning services via encoded URLs
- **L402** — HTTP payment protocol (RFC draft) that gates resources behind a Lightning invoice. Servers return HTTP 402 with a macaroon + invoice; clients pay and retry with the token.

## Environment

- Requires `bash` and Node.js 22.4+ (all commands, including the non-custodial `spark-*` commands, `l402-pay --spark`, and WebSocket subscriptions).
- **Credentials depend on the command** — no single env var is required skill-wide:
  - **Credential-free** (no key, no seed): `resolve-receiver`, `create-invoice-lnaddress`. These use public LNURL-pay on `blink.sv`.
  - **Custodial commands** need `BLINK_API_KEY` with the appropriate scopes.
  - **Non-custodial (Spark) commands** (`spark-balance`, `spark-send`, `spark-fee-probe`, `spark-transactions`, `spark-subscribe`, `spark-info`, `spark-token-info`, `spark-receive-token`, `spark-lnaddress`, and `l402-pay --spark`) need `SPARK_MNEMONIC` (the account seed — spend authority) plus `BREEZ_API_KEY`.
- **Zero _required_ runtime npm dependencies.** The custodial and credential-free commands use only Node.js built-ins (`node:util`, `node:fs`, `node:path`, `node:child_process`). Two **optional, lazy-loaded** dependencies exist solely for the `spark-*` commands and `l402-pay --spark`, and are loaded only when one runs: `@breeztech/breez-sdk-spark` and `bip39`.

Use this skill for concrete wallet operations, not generic Lightning theory.

## Getting Started

### 1. Get your API key

1. Create a free account at [dashboard.blink.sv](https://dashboard.blink.sv).
2. Go to **API Keys** and create a key with the scopes you need.
3. Set it in your environment:

```bash
export BLINK_API_KEY="blink_..."
```

**API Key Scopes:**

- **Read** — query balances, transaction history, price, account info
- **Receive** — create invoices
- **Write** — send payments (use with caution)

> **Tip:** Start with Read + Receive only. Add Write when you need to send payments.

### 2. Verify it works

```bash
node {baseDir}/scripts/balance.js
```

If you see JSON with your wallet balances, you're ready.

### 3. Staging / Testnet (recommended for first-time setup)

To use the Blink staging environment (signet) instead of real money:

```bash
export BLINK_API_URL="https://api.staging.blink.sv/graphql"

Overrides must be `https://`/`wss://` (plaintext only for literal `localhost`/`127.0.0.1` — regtest/dev), and hosts outside `*.blink.sv` additionally require `BLINK_ALLOW_CUSTOM_AUTH_HOST=1` so the API key cannot be silently pointed at an arbitrary host (v2.6.1). The http→ws auto-downgrade was removed: https API hosts derive wss sockets.
```

Create a staging API key at [dashboard.staging.blink.sv](https://dashboard.staging.blink.sv). The staging environment uses signet bitcoin (no real value) — perfect for testing payment flows safely.

If `BLINK_API_URL` is not set, production (`https://api.blink.sv/graphql`) is used by default.

> **Non-custodial note:** `BLINK_API_URL` staging applies to custodial commands only. The `spark-*` commands target Spark mainnet by default; set `SPARK_NETWORK=regtest` (or pass `--network regtest`) for Spark regtest. See [non-custodial](references/non-custodial.md).

### API key resolution

Scripts read `BLINK_API_KEY` from the process environment only:

1. `process.env.BLINK_API_KEY`

No filesystem fallback: shell rc files (`~/.bashrc`, `~/.profile`, etc.) are never read. Export the key in your shell or agent environment before running scripts.

### Optional: CLI wrapper (full GitHub repo only)

If you have cloned the [full GitHub repo](https://github.com/blinkbitcoin/blink-skills), you can optionally install a `blink` CLI command:

```bash
npm install   # install dev dependencies (eslint, prettier)
npm link      # creates global 'blink' command
blink --help  # verify
```

> **Note:** `npm link` modifies global npm state. This is optional — all functionality is available by running scripts directly with `node {baseDir}/scripts/<script>.js`. The ClawHub-installed version does not require or use `npm link`. **Scripts that move money parse options strictly (v3.0.3):** `pay_invoice`, `pay_lnaddress`, `pay_lnurl`, `fee_probe`, `l402_pay`, `spark_send`, and `spark_fee_probe` accept `--opt value` and `--opt=value`. They **refuse**, with exit 1 and before anything is sent, an unknown or misspelled option (e.g. `--dryrun`), a missing value (a trailing `--max-amount`), and a value on a yes/no flag (`--dry-run=true`). Before v3.0.3, such arguments were silently ignored: a ceiling could vanish, or a dry run could become a real payment. The `blink` CLI already behaved this way. **Since v3.0.4 every script parses this way**, including invoices, subscriptions, listings, `l402-discover`, `l402-store` and all `spark-*` commands. For example, `spark-lnaddress delete --network=regtest` used to delete the **mainnet** address, and `l402-store clear --expird` cleared every token. **Memo words that start with a dash go after `--`**, e.g. `blink create-invoice 1000 --no-subscribe -- -50% off`; this applies both at the CLI and when running a script directly. `--` is accepted **only** by commands that take free text (memos and descriptions); anywhere else it is refused. **Unexpected extra arguments are refused too**, not ignored: `l402-store clear expird` (a typo without dashes) used to clear every token, and now exits 1 with the store untouched. Likewise `spark-lnaddress delete alice`, `budget status extra` and `price --usd 5 100` are refused. **Since v3.0.5, a repeated option with a different value is refused** instead of silently keeping the last one: `--network regtest --network mainnet` and `--store --no-store` exit 1. An identical repeat is fine, and repeatable options such as `--header` are unaffected. **Refusal messages name the option or the position, never the value** (e.g. `Conflicting values for --token: give it once`, `unexpected extra argument at position 2`), so a token, preimage or seed passed by mistake is not printed back into logs.

## Agent Safety Policy

These rules are mandatory for any AI agent using this skill:

1. **Ask before spending.** Never execute `pay-invoice`, `pay-lnaddress`, `pay-lnurl`, `swap-execute`, or `spark-send` without explicit user confirmation of the amount and recipient.
   - **Non-custodial seed is sacred.** `SPARK_MNEMONIC` grants full spend authority over a self-custodial account. Never log, echo, display, transmit, or write it. It is read only from the environment variable, never from files.
2. **Dry-run first.** For swaps, always run with `--dry-run` before executing for real unless the user explicitly says to skip it.
3. **Check balance before sending.** Always run `balance` before any payment or swap to verify sufficient funds.
4. **Probe fees before paying.** Run `fee-probe` before `pay-invoice` to show the user the fee cost. Note: probing an invoice your OWN wallet issued fails with `CANT_PAY_SELF` (the probe runs a real prepare) — classify ownership with `resolve-receiver` first, and probe with the wallet that will actually pay.
5. **Use minimum scopes.** Only request Write-scoped API keys when send operations are actually needed.
6. **Never log or display the API key.** Treat `BLINK_API_KEY` as a secret. Do not echo it, include it in messages, or write it to files.
7. **Prefer staging for testing.** When the user is testing or learning, suggest setting `BLINK_API_URL` to the staging endpoint.
8. **Respect irreversibility.** Warn the user that Lightning payments and swaps cannot be reversed once executed.
9. **L402 auto-pay requires configuration and confirmation.** `l402-pay` fails closed: it refuses to pay unless an explicit spending budget (`BLINK_BUDGET_HOURLY_SATS` / `BLINK_BUDGET_DAILY_SATS`) and a non-empty domain allowlist (`BLINK_L402_ALLOWED_DOMAINS` or `blink budget allowlist add`) are configured. It also refuses when the invoice amount cannot be decoded or is below 1 satoshi, since no limit can be applied to an unknown or unenforceable sum. Never call `l402-pay` without dry-running first (`--dry-run`) and confirming the satoshi amount with the user. The token cache (`~/.blink/l402-tokens.json`) means subsequent calls may reuse a paid token silently — inform the user when a cached token is used.

## Bitcoin Units

- **BTC wallet** amounts are always in **satoshis** (sats). 1 BTC = 100,000,000 sats.
- **USD wallet** amounts are always in **cents**. $1.00 = 100 cents.
- When displaying amounts to users, use the formatted fields from output JSON (e.g. `btcBalanceUsdFormatted`, `usdBalanceFormatted`).
- Do not perform manual BTC-to-USD conversion math — use `blink price <sats>` or the `btcBalanceUsd` field from `balance` output instead.
- For swap amounts, the `--unit` flag controls interpretation: `sats` for BTC, `cents` for USD.

## Workflow

1. Pick the operation path first:

- Receive payments (invoice creation, QR codes, payment monitoring).
- Send payments (invoice pay, Lightning Address, LNURL, BTC or USD wallet).
- Swap between wallets (BTC <-> USD internal conversion).
- Read-only queries (balance, transactions, price, account info).
- Non-custodial (Spark) account operations (receive via LNURL, seed-gated balance/send/history/events).

2. Configure API access from [blink-api-and-auth](references/blink-api-and-auth.md):

- Set `BLINK_API_KEY` with the correct scopes for your operation.
- Optionally set `BLINK_API_URL` for staging/testnet.
- Verify connectivity with `blink balance`.

3. For sending payments, follow [payment-operations](references/payment-operations.md):

- Check balance before sending.
- Probe fees with `blink fee-probe`.
- Choose BTC or USD wallet with `--wallet` flag.
- Execute payment and verify in transaction history.

4. For receiving payments, follow [invoice-lifecycle](references/invoice-lifecycle.md):

- Create BTC or USD invoice.
- Parse two-phase output (invoice created, then payment resolution).
- Generate QR code and send to payer.
- Monitor via auto-subscribe, polling, or standalone subscription.

5. For swapping between wallets, follow [swap-operations](references/swap-operations.md):

- Quote first with `blink swap-quote`.
- Review quote terms (amountIn/amountOut, exchange rate).
- Execute with `blink swap-execute` (use `--dry-run` first).
- Verify settlement from `postBalance`/`balanceDelta`.

6. For accessing L402-gated services:

- Discover price with `blink l402-discover <url>` (no payment needed).
- Dry-run with `blink l402-pay <url> --dry-run` and confirm cost with user.
- Pay with `blink l402-pay <url> --max-amount <sats>` (Write scope required).
- Token is cached; subsequent requests reuse it without re-paying.

7. For non-custodial (Spark) accounts, follow [non-custodial](references/non-custodial.md):

- Resolve a `user@blink.sv` recipient with `blink resolve-receiver` (credential-free).
- Receive with `blink create-invoice-lnaddress` (credential-free, works for both account types).
- Balance / send / history / events need `SPARK_MNEMONIC` + `BREEZ_API_KEY` (Node 22.4+).
- Probe fees with `spark-fee-probe` (or `spark-send --dry-run`) first; budget limits apply when configured.

8. Apply safety constraints:

- Use minimum API key scopes for the task.
- Test on staging before production.
- Always check balance before sending.
- Payments are irreversible once settled.

## Quick Commands

```bash
# Check balances
blink balance

# Create BTC invoice (auto-subscribes to payment)
blink create-invoice 1000 "Payment for service"

# Pay a Lightning invoice
blink pay-invoice lnbc1000n1...

# Pay from USD wallet
blink pay-invoice lnbc1000n1... --wallet USD

# Get current BTC/USD price
blink price

# Swap 1000 sats to USD
blink swap-execute btc-to-usd 1000

# Get swap quote without executing
blink swap-quote usd-to-btc 500 --unit cents

# Probe an L402-gated URL (discover price without paying)
blink l402-discover https://api.example.com/resource

# Pay for an L402-gated resource (dry-run first)
blink l402-pay https://api.example.com/resource --dry-run
blink l402-pay https://api.example.com/resource --max-amount 1000

# List cached L402 tokens
blink l402-store list

# Classify a Blink Lightning Address (custodial vs non-custodial Spark)
blink resolve-receiver alice@blink.sv

# Receive to any Blink Lightning Address — no API key, no seed
blink create-invoice-lnaddress alice@blink.sv 1000 "Coffee"

# Non-custodial (Spark) account: balance, fee probe, history
blink spark-balance
blink spark-fee-probe lnbc1000n1... 1000
blink spark-transactions --limit 5
```

## Core Commands

### Check Wallet Balances

```bash
blink balance
```

Returns JSON with all wallet balances (BTC in sats, USD in cents), wallet IDs, pending incoming amounts, and a **pre-computed USD estimate** for the BTC wallet. Use `btcBalanceUsd` for the BTC wallet's USD value — do not calculate it yourself.

### Create Lightning Invoice (BTC)

```bash
blink create-invoice <amount_sats> [--timeout <seconds>] [--no-subscribe] [memo...]
```

Generates a BOLT-11 Lightning invoice for the specified amount in satoshis. Returns the `paymentRequest` string that can be paid by any Lightning wallet. The BTC wallet ID is resolved automatically.

**Auto-subscribe**: After creating the invoice, the script automatically opens a WebSocket subscription and waits for payment. It outputs **two JSON objects** to stdout:

1. **Immediately** — `{"event": "invoice_created", ...}` with `paymentRequest`, `paymentHash`, etc.
2. **When resolved** — `{"event": "subscription_result", "status": "PAID"|"EXPIRED"|"TIMEOUT", ...}`

The agent should read the first JSON to share the invoice/QR with the user right away, then wait for the second JSON to confirm payment.

- `amount_sats` — amount in satoshis (required)
- `--timeout <seconds>` — subscription timeout (default: 300). Use 0 for no timeout.
- `--no-subscribe` — skip WebSocket auto-subscribe, just create the invoice and exit
- `memo...` — optional description attached to the invoice (remaining args joined)

### Create Lightning Invoice (USD)

```bash
blink create-invoice-usd <amount_cents> [--timeout <seconds>] [--no-subscribe] [memo...]
```

Creates a Lightning invoice denominated in USD cents. The sender pays in BTC/Lightning, but the received amount is locked to a USD value at the current exchange rate. Credited to the USD wallet. **Expires in ~5 minutes** due to exchange rate lock.

**Auto-subscribe**: Same two-phase output as `create-invoice` — first JSON is the created invoice, second JSON is the payment resolution (PAID/EXPIRED/TIMEOUT).

- `amount_cents` — amount in USD cents, e.g. 100 = $1.00 (required)
- `--timeout <seconds>` — subscription timeout (default: 300). Use 0 for no timeout.
- `--no-subscribe` — skip WebSocket auto-subscribe, just create the invoice and exit
- `memo...` — optional description attached to the invoice (remaining args joined)

### Check Invoice Status

```bash
blink check-invoice <payment_hash>
```

Checks the payment status of a Lightning invoice by its payment hash. Use after creating an invoice to detect when it has been paid. Returns status: `PAID`, `PENDING`, or `EXPIRED`.

- `payment_hash` — the 64-char hex payment hash from `create-invoice` output (required)

### Pay Lightning Invoice

```bash
blink pay-invoice <bolt11_invoice> [--wallet BTC|USD] [--max-amount <sats>]
```

Pays a BOLT-11 Lightning invoice from the BTC or USD wallet. Returns payment status: `SUCCESS`, `PENDING`, `FAILURE`, or `ALREADY_PAID`. The wallet ID is resolved automatically.

- `bolt11_invoice` — the BOLT-11 payment request string, e.g. `lnbc...` (required)
- `--wallet BTC|USD` — wallet to pay from (default: BTC). When USD is selected, the Blink API debits the USD equivalent from the USD wallet.
- `--max-amount <sats>` — refuse, **before any API call**, if the invoice charges more than N sats (the same conservative charge the budget uses: rounded up, at least 1 sat). Applies to `--dry-run` too and is **not** bypassed by `--force`. If the invoice amount can't be decoded, a requested ceiling refuses the payment. Before v3.0.3 the script silently ignored this flag (and `blink pay-invoice` didn't accept it).

**Requires Write scope on the API key.**

> **AGENT:** This command spends funds. Always run `balance` and `fee-probe` first, then confirm amount and recipient with the user before executing.

### Pay to Lightning Address

```bash
blink pay-lnaddress <lightning_address> <amount_sats> [--wallet BTC|USD]
```

Sends satoshis to a Lightning Address (e.g. `user@blink.sv`). Returns payment status. The wallet ID is resolved automatically.

- `lightning_address` — recipient in `user@domain` format (required)
- `amount_sats` — amount in satoshis (required)
- `--wallet BTC|USD` — wallet to pay from (default: BTC). When USD is selected, the amount is still specified in satoshis; the Blink API debits the USD equivalent from the USD wallet automatically.

**Requires Write scope on the API key.**

> **AGENT:** This command spends funds. Always run `balance` first, confirm the Lightning Address and amount with the user, then execute.

### Pay to LNURL

```bash
blink pay-lnurl <lnurl> <amount_sats> [--wallet BTC|USD]
```

Sends satoshis to a raw LNURL payRequest string. For Lightning Addresses (`user@domain`), use `pay-lnaddress` instead.

- `lnurl` — LNURL string, e.g. `lnurl1...` (required)
- `amount_sats` — amount in satoshis (required)
- `--wallet BTC|USD` — wallet to pay from (default: BTC). When USD is selected, the amount is still specified in satoshis; the Blink API debits the USD equivalent from the USD wallet automatically.

**Requires Write scope on the API key.**

> **AGENT:** This command spends funds. Always run `balance` first, confirm the LNURL and amount with the user, then execute.

### Estimate Payment Fee

```bash
blink fee-probe <bolt11_invoice> [--wallet BTC|USD]
```

Estimates the fee for paying a Lightning invoice without actually sending. Use before `pay-invoice` to check costs. Payments to other Blink users and direct-channel nodes are free (0 sats).

- `bolt11_invoice` — the BOLT-11 payment request string (required)
- `--wallet BTC|USD` — wallet to probe from (default: BTC). When USD is selected, uses `lnUsdInvoiceFeeProbe` to estimate fees from the USD wallet's perspective.

### Render Invoice QR Code

```bash
blink qr <bolt11_invoice>
```

Renders a terminal QR code for a Lightning invoice (BOLT-11) to stderr and generates a **PNG image file** in a private temp directory. The stdout JSON includes a `pngPath` field with the absolute path to the PNG file. Always use `pngPath`; do not guess the location.

**Sending the QR image to a user**: After running this script, use the `pngPath` from the JSON output to send the PNG as a media attachment to the user in the current chat. The agent should use its native message-send capability with the file path.

- `bolt11_invoice` — the BOLT-11 payment request string (required)

Output JSON includes:

- `invoice` — uppercased invoice string
- `qrRendered` — always `true`
- `qrSize` — QR module count
- `errorCorrection` — `"L"` (LOW)
- `pngPath` — absolute path to the generated PNG file (e.g. `/tmp/blink-qr-Ab12Cd/invoice.png`: a fresh `0700` directory under the system temp dir, `TMPDIR` honored, holding a `0600` file)
- `pngBytes` — file size in bytes

### List Transactions

```bash
blink transactions [--first N] [--after CURSOR] [--wallet BTC|USD]
```

Lists recent transactions (incoming and outgoing) with pagination. Returns direction, amount, status, type (lightning/onchain/intraledger), and metadata. Settlement **preimages are suppressed by default** — they are reusable L402 bearer credentials (a field-test cross-reference recovered 3 of 4 cached L402 tokens verbatim from this listing); pass `--include-preimage` only for deliberate proof-of-payment export. `paymentHash`, the non-secret correlator, is always present.

- `--first N` — number of transactions to return (default: 20, max: 100)
- `--after CURSOR` — pagination cursor from previous response's `endCursor`
- `--include-preimage` — include settlement preimages in the output (deliberate proof-of-payment export; suppressed by default)
- `--wallet BTC|USD` — filter to a specific wallet currency

### Get BTC/USD Price

```bash
blink price [amount_sats]
blink price --usd <amount_usd>
blink price --history <range>
blink price --currencies
```

Multi-purpose exchange rate tool. All price queries are **public (no API key required)**, though the key is sent if available.

**Modes:**

- **No args** — current BTC/USD price and sats-per-dollar rate
- **`<amount_sats>`** — convert a satoshi amount to USD (e.g. `blink price 1760` → `$1.20`)
- **`--usd <amount>`** — convert a USD amount to sats (e.g. `blink price --usd 5.00` → `7350 sats`)
- **`--history <range>`** — historical BTC price data with summary stats (high/low/change). Ranges: `ONE_DAY`, `ONE_WEEK`, `ONE_MONTH`, `ONE_YEAR`, `FIVE_YEARS`
- **`--currencies`** — list all supported display currencies (IDs, names, symbols, flags)

### Account Info

```bash
blink account-info
```

Shows account level, spending limits (withdrawal, internal send, convert), default wallet, and wallet summary with **pre-computed USD estimates** for BTC balances. Limits are denominated in USD cents with a rolling 24-hour window.

## Non-Custodial (Spark) Commands

Full details, setup, and security model: [non-custodial](references/non-custodial.md).

### Resolve a Blink Receiver (account-type classifier)

```bash
blink resolve-receiver <identifier>   # e.g. alice  or  alice@blink.sv
```

Classifies a Blink identifier (bare username or `user@blink.sv`) as `custodial` (has a Blink wallet ID) or `lnaddress` (non-custodial Spark, served by the LNURL server), or reports it does not exist. **Credential-free** (`BLINK_API_KEY` optional, improves the custodial probe).

### Receive to Any Blink Lightning Address

```bash
blink create-invoice-lnaddress <lightning_address> <amount_sats> [memo...] [--timeout <seconds>] [--no-verify]
```

Mints a BOLT-11 invoice for any `user@blink.sv` recipient via public LNURL-pay — **no API key and no seed required**, and it works whether the recipient is custodial or non-custodial (Spark); the LNURL server routes internally. Classification first sends an unauthenticated `accountDefaultWallet` request to the Blink API host (`BLINK_API_URL`); if that probe fails at the transport level, the command aborts (`CUSTODIAL_PROBE_FAILED`) instead of guessing the account type. It outputs `invoice_created` immediately; a second JSON object follows **only when settlement polling is active** (see below). For Spark recipients the settled flag is webhook-populated and can lag a few seconds.

- `--timeout <seconds>` — verify-poll timeout (default: 300, 0 = no timeout)
- `--no-verify` — skip settlement polling; just create the invoice and exit

**Output cardinality is conditional.** `invoice_created` is always emitted. The second object (`verify_result`, `PAID`/`TIMEOUT`) follows only if polling is active: `--no-verify` was **not** passed **and** the first JSON contains a `verifyUrl`. Check `verifyUrl` in the first JSON before waiting — when it is absent, the command emits exactly one object and exits.

- `--qr` — render a terminal QR (stderr) and a PNG (in a private temp directory, see `qr`) for the minted invoice; QR fields (`pngPath`, `qrSize`, `pngBytes`, …) are merged into the `invoice_created` JSON

### Spark Info

```bash
blink spark-info [--network mainnet|regtest]
```

Shows a Spark account's info from the SDK's `getInfo()` — balance plus any other fields the SDK version returns. SDK values are normalized for JSON: safe-integer BigInts become **numbers**, BigInts outside the safe range become **decimal strings**, and SDK Maps (e.g. `tokenBalances`) become **plain objects**. Non-custodial counterpart of `account-info`. Requires `SPARK_MNEMONIC` + `BREEZ_API_KEY`.

### Spark Balance

```bash
blink spark-balance [--network mainnet|regtest]
```

Reads the BTC balance of a self-custodial (Spark) account directly from the wallet via the Breez Spark SDK — non-custodial balances are **not visible through the Blink API** — waiting briefly for a stable read after incoming payments (`stable` field), **plus `tokenBalances`** for every BTKN token held (USDB etc.): each entry carries the precision-preserving `balance` (string), `balanceFormatted`, and the token metadata (`ticker`, `decimals`, `name`).

### Spark Token Info

```bash
blink spark-token-info <usdb|identifier> [--network mainnet|regtest]
```

Fetches BTKN token metadata (name, ticker, **decimals**, max supply, issuer) — resolves the decimal precision before sending token amounts, and verifies identifiers. The `usdb` alias resolves per-network: `SPARK_USDB_TOKEN` env var, then the documented mainnet constant (Brale-issued USDB, 6 decimals); on regtest the alias fails with the `SPARK_USDB_TOKEN` hint unless set.

### Spark Receive Token

```bash
blink spark-receive-token <amount> [--token usdb|<identifier>] [--base-units] [--description "..."] [--network mainnet|regtest]
```

Mints a **Spark invoice** for receiving a BTKN token (e.g. USDB) into the self-custodial wallet — the `paymentRequest` string can be paid by any Spark wallet. The amount is decimal token units (`25` = 25 USDB, resolved via metadata decimals) or raw base units with `--base-units`. This is a Spark invoice, **not** a BOLT-11 Lightning invoice — the non-custodial counterpart of `create-invoice-usd` over Lightning does not exist (LNURL-pay receive is BTC-only); this is the token-native receive path.

### Spark LN Address

```bash
blink spark-lnaddress get
blink spark-lnaddress check <username>
blink spark-lnaddress register <username> [--description "..."]
blink spark-lnaddress delete
```

Manages the self-custodial wallet's registered **`user@blink.sv`** Lightning address via the SDK. All operations run against the **Blink domain** — pinned by `_spark_sdk.connect()` (`lnurlDomainFor`: `blink.sv` on mainnet, `staging.blink.sv` on regtest, `SPARK_LNURL_DOMAIN` override for other Blink deployments; `breez.tips`, the Breez SDK's default, is **refused**).

- `get` — reports the registered address. The SDK recovers it automatically on connect (keyed by the seed-derived identity pubkey), so **a seed imported from blink-mobile with a registered address is discoverable from the seed alone**. `registered` is three-state: `true` (address from the recovery cache), `false` (verified negative — the lookup service answered a probe), or `"unknown"` (service unreachable; **exit 1** — the answer cannot be trusted, do not register/delete). The probe exists because recovery fails silently inside the SDK when the LNURL service is down (observed live 2026-09-12: `registered: false` while a registered address existed).
- `check <username>` — server-side availability (a uniqueness lookup across BOTH account providers: an available name is claimable by anyone).
- `register <username>` — claims the username on the wallet's pubkey. One username per pubkey per domain — **a new registration replaces the wallet's previous one**. Usernames: 3–50 chars `[a-z0-9_]`, ≥1 letter; uppercase is rejected client-side — never silently normalized onto the network. Confirms availability first; exits 1 on `UNAVAILABLE`. No funds move.
- `delete` — removes the address (reversible by re-registering, subject to availability).

`spark-info` also reports the recovered `lightningAddress`, a `lnAddressStatus` (`registered` | `none` = verified negative | `unverified` = service unreachable — null then means "cannot know", not "no address"), and the pinned `lnurlDomain`. Since v2.4.0 spark outputs carry `accountType: 'spark'` (the wallet kind); whether a Lightning address is registered is the `lightningAddress` / `lnAddressStatus` pair, never the accountType. (`create-invoice-lnaddress` and `resolve-receiver` still classify a _receiver_ as `type: 'lnaddress'` when an address is Spark-backed — a different field, a different vocabulary.)

> **Never compose a three-state field into another command via shell substitution.** `lnAddressStatus: "unverified"` / `registered: "unknown"` mean the address is UNKNOWN — a shell `$(… lightningAddress …)` yields an empty string that downstream commands resolve against a DEFAULT, not against your wallet. Live near-miss (FT6): an empty address composed into `create-invoice-lnaddress` resolved as `none@blink.sv` — a real third-party custodial wallet. When the status is not `registered`, treat the address as absent; `resolve-receiver` your own known address first and verify the pubkey before paying.

> **AGENT:** Confirm the username with the user before `register` — it is a public identity choice — and warn that registration replaces any previous address.

### Spark Send

```bash
blink spark-send <destination> <amount_sats> [--dry-run] [--force] [--network mainnet|regtest]

# Token mode (BTKN, e.g. USDB):
blink spark-send <spark-address-or-invoice> <amount> --token usdb|<identifier> [--base-units]
blink spark-send <spark-address-or-invoice> <amount> --token <id> --from-btc [--slippage-bps <n>]
blink spark-send <bolt11-invoice> <amount_sats> --from-token usdb|<identifier> [--slippage-bps <n>]
```

Signs and sends BTC from a Spark account **locally with the seed** — no Blink API involvement. Destinations are classified **exhaustively**: only BOLT-11 invoices, Spark addresses/invoices, Lightning Addresses, and LNURL-pay URLs are accepted (a Lightning Address uses the LNURL-pay path). Anything else the SDK recognizes — on-chain Bitcoin addresses, BOLT-12 offers, cross-chain destinations — is rejected with `UNSUPPORTED_DESTINATION` before any prepare or budget interaction, and `destinationType` in the output is `bolt11`, `spark`, or `lnurl` accordingly. The prepare step **attempts** to resolve fees and reports them as `feeSats` before sending; `feeSats` may be `null` (printed as `unknown`) when the SDK response shape is unrecognized — treat the fee as unknown and say so to the user before executing. `--dry-run` stops after the prepare step and moves nothing. Exits non-zero if the SDK reports a `failed` payment status.

Subject to the same budget controls as the custodial pay commands: configured limits (`BLINK_BUDGET_HOURLY_SATS` / `BLINK_BUDGET_DAILY_SATS`) are enforced after fee resolution and before signing; an unconfigured budget does not block this explicit one-shot payment. Successful/pending sends are recorded in the spending log (a failed recording warns on stderr but never masks the payment result). `--force` bypasses the budget check for an over-limit send. **Budgets count the payment principal (the amount), not the routing fee** — the same convention as the custodial pay commands.

**Token mode** (USDB and other BTKN tokens): `--token` sends tokens to a Spark address or Spark invoice; the amount is decimal token units (`10.5` USDB) resolved via the token's decimals, or raw base units with `--base-units` (`10500000` = 10.5 USDB at 6 decimals). `--from-btc` pays a token send by converting BTC on the fly — the **sats side of the conversion estimate is budget-enforced**, an absent/zero/unusable estimate refuses to dispatch unless `--force` is passed, and outcome-unknown post-dispatch errors keep the reservation fail-closed (only an explicit terminal `failed` releases it). `--from-token` pays a BOLT-11 invoice by converting tokens: the **invoice's BTC amount is authoritative** — a supplied amount that mismatches the invoice is rejected before dispatch (dry-runs included), and outputs emit the authoritative amount. No sats leave the wallet on `--from-token`, so the sats budget does not apply (tokens are spent). `--slippage-bps` caps conversion slippage (default 50 bps; failed conversions auto-refund per the SDK). Plain token sends are outside the sats budget by design. The `conversionEstimate` in the prepare output (`amountIn` source asset → `amountOut` target asset, `fee`) is the quote — dry-run or `spark-fee-probe` to see it without sending.

**Live-tested conversion facts (field test 3):** the minimum conversion is **800 sats** per `--from-btc` leg — budget ≥1000 sats per leg (sub-minimum amounts abort with `Amount … is less than minimum required 800`). Conversion spreads are tight (~0.1–0.12% round-trip vs ~1.7% on custodial cent-granularity swaps — token decimals, not fee schedules). Two SDK constraints: a **token-only send to your own invoice is refused** (`Self payment not allowed`) — a `--from-btc` conversion to the same invoice works (conversions are not transfers), so single-wallet token testing uses conversions, and a genuine wallet→wallet token transfer needs a second wallet. Receiving via BOLT-11 (an app-minted USD Lightning invoice) credits USDB server-side with spark sats unchanged.

In `spark-transactions` output, token rows carry `asset: "token"` with `amountBaseUnits` (precision string), `amountFormatted`, and `token` metadata — `amountSats` is `null` on token rows (base units are not sats; a $0.999 USDB receive is `999001` base units, never "999,001 sats"). BTC rows carry `asset: "btc"` and the usual `amountSats`/`feeSats`.

> **AGENT:** This command spends self-custodial funds irreversibly. Probe the fee (`spark-fee-probe` or `--dry-run`) first, then confirm the amount and destination with the user before executing.

### Spark Fee Probe

```bash
blink spark-fee-probe <destination> <amount_sats> [--network mainnet|regtest]
blink spark-fee-probe <spark-address> <amount> --token usdb|<identifier> [--from-btc]
blink spark-fee-probe <bolt11-invoice> <amount_sats> --from-token usdb|<identifier>
```

Estimates the fee for sending from a Spark account **without sending** — it runs the same prepare step as `spark-send` and stops there. Same exhaustive destination allowlist as `spark-send`. Non-custodial counterpart of `fee-probe`; use it before `spark-send` to check costs. Nothing is signed, nothing moves, nothing is recorded. Token/conversion flags are supported — the probe returns the `conversionEstimate` (the quote) alongside the fee.

### Spark Transactions

```bash
blink spark-transactions [--limit <n>] [--offset <n>] [--type send|receive] [--network mainnet|regtest]
```

Lists recent Spark account payments from SDK-local history: `--limit` (default 20), `--offset` for pagination, `--type send|receive` to filter by direction. Output includes a `pageInfo` block — `hasNextPage` is `true` only when the page came back full. This history is invisible to the Blink API.

### Spark Subscribe

```bash
blink spark-subscribe [--timeout <seconds>] [--network mainnet|regtest]
```

Streams live Spark wallet events as NDJSON (one JSON line per event). `--timeout` stops after N seconds (default: 300, 0 = run until interrupted). Non-custodial counterpart of `subscribe-updates`. Since Breez SDK 0.25.0 the event stream can also surface `unilateralExitStateChanged` (wallet unilateral-exit state transitions) — watch for it if you rely on exit tooling; it is informational only and not yet interpreted by any skill command.

> All `spark-*` commands require `SPARK_MNEMONIC` + `BREEZ_API_KEY` and Node 22.4+. Network defaults to mainnet; `SPARK_NETWORK` env var or `--network` flag overrides. See the Environment section above and [non-custodial](references/non-custodial.md) for getting a Breez key and installing the optional SDK dependencies.

## Realtime Subscriptions

Blink supports GraphQL subscriptions over WebSocket using the `graphql-transport-ws` protocol. Uses the native WebSocket built into Node 22.4+ (no flags needed).

### Subscribe to Invoice Payment Status

```bash
blink subscribe-invoice <bolt11_invoice> [--timeout <seconds>]
```

Watches a single invoice and exits when it is **PAID** or **EXPIRED**. Status updates are printed to stderr. JSON result is printed to stdout.

### Subscribe to Account Updates (myUpdates)

```bash
blink subscribe-updates [--timeout <seconds>] [--max <count>]
```

Streams account updates in real time. Each event is output as a JSON line (NDJSON) to stdout. Use `--max` to stop after N events.

## API Reference

| Operation          | GraphQL                                                                                           | Scope Required              |
| ------------------ | ------------------------------------------------------------------------------------------------- | --------------------------- |
| Check balance      | `query me` + `currencyConversionEstimation`                                                       | Read                        |
| Create BTC invoice | `mutation lnInvoiceCreate`                                                                        | Receive                     |
| Create USD invoice | `mutation lnUsdInvoiceCreate`                                                                     | Receive                     |
| Check invoice      | `query invoiceByPaymentHash`                                                                      | Read                        |
| Pay invoice        | `mutation lnInvoicePaymentSend`                                                                   | Write                       |
| Pay LN address     | `mutation lnAddressPaymentSend`                                                                   | Write                       |
| Pay LNURL          | `mutation lnurlPaymentSend`                                                                       | Write                       |
| Fee estimate (BTC) | `mutation lnInvoiceFeeProbe`                                                                      | Read                        |
| Fee estimate (USD) | `mutation lnUsdInvoiceFeeProbe`                                                                   | Read                        |
| Swap BTC→USD       | `mutation intraLedgerPaymentSend`                                                                 | Write                       |
| Swap USD→BTC       | `mutation intraLedgerUsdPaymentSend`                                                              | Write                       |
| Transactions       | `query transactions`                                                                              | Read                        |
| Price / convert    | `query currencyConversionEstimation`                                                              | **None (public)**           |
| Price history      | `query btcPriceList`                                                                              | **None (public)**           |
| Currency list      | `query currencyList`                                                                              | **None (public)**           |
| Realtime price     | `query realtimePrice`                                                                             | **None (public)**           |
| Account info       | `query me` + `currencyConversionEstimation`                                                       | Read                        |
| Subscribe invoice  | `subscription lnInvoicePaymentStatus`                                                             | Read                        |
| Subscribe updates  | `subscription myUpdates`                                                                          | Read                        |
| L402 discover      | external HTTP (no Blink API)                                                                      | **None**                    |
| L402 pay           | `mutation lnInvoicePaymentSend` (on 402)                                                          | Write                       |
| Resolve receiver   | unauthenticated `accountDefaultWallet` probe (Blink GraphQL) + `.well-known/lnurlp` (public HTTP) | **None (public)**           |
| Invoice via LNURL  | unauthenticated `accountDefaultWallet` probe (Blink GraphQL) + LNURL-pay (LUD-06/16/21)           | **None (public)**           |
| Spark balance      | Breez Spark SDK (no Blink API)                                                                    | **Seed** (`SPARK_MNEMONIC`) |
| Spark send         | Breez Spark SDK (no Blink API)                                                                    | **Seed** (`SPARK_MNEMONIC`) |
| Spark transactions | Breez Spark SDK (no Blink API)                                                                    | **Seed** (`SPARK_MNEMONIC`) |
| Spark subscribe    | Breez Spark SDK events (no Blink API)                                                             | **Seed** (`SPARK_MNEMONIC`) |

**API Endpoint:** `https://api.blink.sv/graphql` (production)
**Authentication:** `X-API-KEY` header

**USD wallet notes:** The `lnInvoicePaymentSend`, `lnAddressPaymentSend`, and `lnurlPaymentSend` mutations all accept either a BTC or USD wallet ID. When a USD wallet ID is provided, the API debits the USD equivalent automatically. Amounts for `lnAddressPaymentSend` and `lnurlPaymentSend` are always specified in satoshis regardless of wallet type.

## Output Format

All commands output structured JSON to stdout. Status messages and errors go to stderr. Exit code 0 on success, 1 on failure.

### Balance output example

```json
{
  "wallets": [
    { "id": "abc123", "currency": "BTC", "balance": 1760, "unit": "sats" },
    { "id": "def456", "currency": "USD", "balance": 1500, "unit": "cents" }
  ],
  "btcWalletId": "abc123",
  "btcBalance": 1760,
  "btcBalanceSats": 1760,
  "btcBalanceUsd": 1.2,
  "btcBalanceUsdFormatted": "$1.20",
  "usdWalletId": "def456",
  "usdBalance": 1500,
  "usdBalanceCents": 1500,
  "usdBalanceFormatted": "$15.00"
}
```

### Invoice creation output example (two-phase)

First JSON (immediate):

```json
{
  "event": "invoice_created",
  "paymentRequest": "lnbc500n1...",
  "paymentHash": "abc123...",
  "satoshis": 500,
  "status": "PENDING",
  "createdAt": "2026-02-23T00:00:00Z",
  "walletId": "abc123"
}
```

Second JSON (when payment resolves):

```json
{
  "event": "subscription_result",
  "paymentRequest": "lnbc500n1...",
  "status": "PAID",
  "isPaid": true,
  "isExpired": false,
  "isPending": false
}
```

### Invoice status output example

```json
{
  "paymentHash": "abc123...",
  "paymentStatus": "PAID",
  "satoshis": 500,
  "isPaid": true,
  "isExpired": false,
  "isPending": false
}
```

### Payment output example (BTC wallet)

```json
{
  "status": "SUCCESS",
  "walletId": "abc123",
  "walletCurrency": "BTC",
  "balanceBefore": 50000
}
```

### Payment output example (USD wallet)

```json
{
  "status": "SUCCESS",
  "walletId": "def456",
  "walletCurrency": "USD",
  "balanceBefore": 1500,
  "balanceBeforeFormatted": "$15.00"
}
```

### Price output example

```json
{
  "btcPriceUsd": 68036.95,
  "satsPerDollar": 1470,
  "conversion": {
    "sats": 1760,
    "usd": 1.2,
    "usdFormatted": "$1.20"
  }
}
```

### USD-to-sats conversion output example

```json
{
  "btcPriceUsd": 68036.95,
  "satsPerDollar": 1470,
  "conversion": {
    "usd": 5.0,
    "usdFormatted": "$5.00",
    "sats": 7350
  }
}
```

### Price history output example

```json
{
  "range": "ONE_DAY",
  "dataPoints": 24,
  "summary": {
    "current": 68036.95,
    "oldest": 67500.0,
    "high": 68500.0,
    "low": 67200.0,
    "changeUsd": 536.95,
    "changePct": 0.8
  },
  "prices": [{ "timestamp": 1740000000, "date": "2025-02-20T00:00:00.000Z", "btcPriceUsd": 67500.0 }]
}
```

### Transaction list output example

```json
{
  "transactions": [
    {
      "id": "tx_123",
      "direction": "RECEIVE",
      "status": "SUCCESS",
      "amount": 1000,
      "currency": "BTC",
      "type": "lightning",
      "paymentHash": "abc...",
      "createdAt": 1740000000
    }
  ],
  "count": 1,
  "pageInfo": {
    "hasNextPage": false,
    "endCursor": "cursor_abc"
  }
}
```

### Resolve receiver output example

```json
{
  "exists": true,
  "type": "lnaddress",
  "username": "alice",
  "domain": "blink.sv",
  "lightningAddress": "alice@blink.sv",
  "walletId": null
}
```

`type` is `"custodial"` when the identifier maps to a Blink wallet (`walletId` present), `"lnaddress"` for a non-custodial (Spark) account. For unknown identifiers: `{ "exists": false, "type": null, ... }`.

### Spark output examples

**spark-balance:**

```json
{
  "accountType": "spark",
  "network": "mainnet",
  "balanceSats": 25000,
  "stable": true
}
```

**spark-send (dry-run):**

```json
{
  "event": "send_prepared",
  "dryRun": true,
  "destination": "alice@blink.sv",
  "destinationType": "lnurl",
  "amountSats": 1000,
  "feeSats": 1,
  "network": "mainnet"
}
```

**spark-send (executed):** same shape with `"event": "send_result"` plus `status` and `paymentId`. Exit code 1 when the SDK reports a `failed` payment status; `pending` exits 0 (still in flight).

**spark-transactions:**

```json
{
  "accountType": "spark",
  "network": "mainnet",
  "count": 2,
  "transactions": [
    {
      "id": "abc123",
      "type": "receive",
      "status": "COMPLETED",
      "asset": "btc",
      "amountSats": 1000,
      "feeSats": 0,
      "timestamp": 1740000000
    },
    {
      "id": "07bc5d3e:0",
      "type": "receive",
      "status": "COMPLETED",
      "asset": "token",
      "amountSats": null,
      "feeSats": null,
      "amountBaseUnits": "999001",
      "feeBaseUnits": "0",
      "amountFormatted": "0.999001",
      "token": { "ticker": "USDB", "name": "USD Beacon", "decimals": 6, "identifier": "btkn1..." },
      "timestamp": 1740000060
    }
  ],
  "pageInfo": { "hasNextPage": false, "limit": 20, "offset": 0 }
}
```

**spark-fee-probe:**

```json
{
  "event": "fee_probe",
  "destination": "lnbc1000n1...",
  "destinationType": "bolt11",
  "amountSats": 1000,
  "feeSats": 1,
  "network": "mainnet"
}
```

**create-invoice-lnaddress (two-phase):** first JSON is `invoice_created` (`accountType`, `lightningAddress`, `paymentRequest`, `verifyUrl`, `satoshis`); second JSON is `verify_result` with `status` `"PAID"` or `"TIMEOUT"` — emitted **only when polling is active**: `--no-verify` was not passed and `verifyUrl` is present in the first JSON. Inspect `verifyUrl` before waiting; without it, exactly one object is emitted.

## Typical Agent Workflows

### Receive a payment (recommended — auto-subscribe + QR image)

```bash
# 1. Create invoice — script auto-subscribes and outputs two JSON objects
blink create-invoice 1000 "Payment for service"
# → First JSON: {"event": "invoice_created", "paymentRequest": "lnbc...", ...}
# → Read paymentRequest from first JSON immediately

# 2. Generate QR code PNG
blink qr <paymentRequest>
# → JSON includes "pngPath": "/tmp/blink-qr-Ab12Cd/invoice.png"
# → Send the PNG file to the user as a media attachment in the current chat

# 3. The create-invoice command is still running, waiting for payment
# → Second JSON: {"event": "subscription_result", "status": "PAID", ...}
# → When PAID: notify the user that payment has been received
# → When EXPIRED: notify the user the invoice expired
```

**Important**: The `create-invoice` command outputs two JSON objects separated by a newline. Parse them as separate JSON objects, not as a single JSON array. The first object arrives immediately; the second arrives when payment status resolves.

### Receive a payment (polling fallback)

```bash
# 1. Create invoice without auto-subscribe
blink create-invoice 1000 --no-subscribe "Payment for service"
# 2. Give the paymentRequest to the payer
# 3. Poll for payment
blink check-invoice <payment_hash>
# 4. Verify balance
blink balance
```

### Receive a USD payment

```bash
# Same two-phase pattern as BTC, but using create-invoice-usd
# Note: USD invoices expire in ~5 minutes
blink create-invoice-usd 500 "Five dollars for service"
# → First JSON: {"event": "invoice_created", "amountCents": 500, "amountUsd": "$5.00", ...}
# Generate QR and send to user, then wait for second JSON
```

### Receive for a non-custodial (Spark) recipient (no credentials)

```bash
# 1. (Optional) classify the recipient
blink resolve-receiver alice@blink.sv
# → {"exists": true, "type": "lnaddress", "lightningAddress": "alice@blink.sv", ...}

# 2. Mint an invoice via public LNURL-pay — no API key, no seed
blink create-invoice-lnaddress alice@blink.sv 1000 "Coffee"
# → First JSON: {"event": "invoice_created", "accountType": "lnaddress", "paymentRequest": "lnbc...", "verifyUrl": "https://...", ...}
# Generate QR from paymentRequest (blink qr works on any BOLT-11) and send to the payer

# 3. If verifyUrl was present (and --no-verify was not passed), wait for the second JSON:
# → {"event": "verify_result", "status": "PAID", ...}
# If verifyUrl is absent, the command already emitted its only JSON object and exited.
# For Spark recipients the settled flag is webhook-populated and can lag a few seconds.
```

### Send from a non-custodial (Spark) account

```bash
# Requires SPARK_MNEMONIC + BREEZ_API_KEY (Node 22.4+)

# 1. Probe the fee (nothing is sent)
blink spark-fee-probe lnbc1000n1... 1000
# → {"event": "fee_probe", "feeSats": 1, ...}

# 2. Check balance
blink spark-balance

# 3. Confirm amount and recipient with the user, then send
blink spark-send lnbc1000n1... 1000
# → {"event": "send_result", "status": "COMPLETED", ...}  (exit 1 on failed)

# 4. Verify in SDK-local history
blink spark-transactions --limit 1
```

### Send a payment (with fee check)

```bash
# 1. Check current balance
blink balance
# 2. Estimate fee
blink fee-probe lnbc1000n1...
# 3. Send payment
blink pay-invoice lnbc1000n1...
# 4. Verify in transaction history
blink transactions --first 1
```

### Send from the USD wallet

```bash
# Pay an invoice from the USD wallet
blink fee-probe lnbc1000n1... --wallet USD
blink pay-invoice lnbc1000n1... --wallet USD

# Send to a Lightning Address from the USD wallet
blink pay-lnaddress user@blink.sv 1000 --wallet USD

# Send via LNURL from the USD wallet
blink pay-lnurl lnurl1... 1000 --wallet USD

# Note: for lnaddress and lnurl, the amount is always in satoshis.
# The Blink API debits the USD equivalent from the USD wallet automatically.
```

### Convert sats to USD value

```bash
# Check how much 1760 sats is worth in USD
blink price 1760
# → $1.20
```

### Convert USD to sats

```bash
# How many sats is $5.00?
blink price --usd 5.00
# → 7350 sats
```

### Swap BTC to USD (internal conversion)

```bash
# 1. Get a quote first
blink swap-quote btc-to-usd 2000
# → Shows expected conversion terms (amountIn: 2000 sats, amountOut: ~136 cents)

# 2. Execute the swap (dry-run first)
blink swap-execute btc-to-usd 2000 --dry-run
# → Shows what would happen without moving funds

# 3. Execute for real
blink swap-execute btc-to-usd 2000
# → Converts 2000 sats from BTC wallet to ~$1.36 in USD wallet

# 4. Verify balances
blink balance
```

### Swap USD to BTC (internal conversion)

```bash
# Convert $5.00 (500 cents) to BTC
blink swap-execute usd-to-btc 500 --unit cents
# → Converts 500 cents from USD wallet to ~7350 sats in BTC wallet
```

### Pay for an L402-gated service

```bash
# 1. Discover what the service costs (no payment)
blink l402-discover https://api.example.com/resource
# → shows satoshis, format, macaroon

# 2. Dry-run to confirm price with user before spending
blink l402-pay https://api.example.com/resource --dry-run
# → {"event": "l402_dry_run", "satoshis": 100, ...}

# 3. Check your balance first
blink balance

# 4. Pay (with optional safety limit)
blink l402-pay https://api.example.com/resource --max-amount 500
# → pays invoice, caches token, returns resource data

# 5. Subsequent calls reuse cached token (no re-payment)
blink l402-pay https://api.example.com/resource
# → {"event": "l402_paid", "tokenReused": true, ...}
```

### Check price history

```bash
# Get BTC price over the last 24 hours
blink price --history ONE_DAY
# Get BTC price over the last month
blink price --history ONE_MONTH
```

## Swap Commands (BTC <-> USD)

Swap between your BTC and USD wallets using Blink's intra-ledger transfer. This is an internal conversion (not a Lightning payment), so there are no routing fees — only minor rounding spread.

### Get Swap Quote

```bash
blink swap-quote <direction> <amount> [--unit sats|cents] [--ttl-seconds N] [--immediate]
```

Estimates the conversion terms without moving funds. Returns wallet balances, exchange rate snapshot, and the expected `amountIn`/`amountOut` in the output JSON.

- `direction` — `btc-to-usd` or `usd-to-btc` (aliases: `sell-btc`, `buy-usd`, `sell-usd`, `buy-btc`)
- `amount` — positive integer amount to convert
- `--unit sats|cents` — unit of the amount (defaults to `sats` for btc-to-usd, `cents` for usd-to-btc)
- `--ttl-seconds N` — quote TTL in seconds (default: 60)
- `--immediate` — flag the quote for immediate execution

**No API key scope beyond Read is required for quotes.**

### Execute Swap

```bash
blink swap-execute <direction> <amount> [--unit sats|cents] [--dry-run] [--memo "text"]
```

Executes a real BTC <-> USD conversion. First generates a quote, then performs the intra-ledger transfer. Returns pre/post balances, delta, quote terms, and transaction ID.

- `direction` — same as swap-quote
- `amount` — positive integer amount to convert
- `--unit sats|cents` — same as swap-quote
- `--dry-run` — show what would be swapped without executing the transfer
- `--memo "text"` — optional memo attached to the transaction

**CAUTION: Without `--dry-run`, this moves real funds between wallets. Requires Write scope.**

> **AGENT:** This command moves funds between wallets. Always run with `--dry-run` first, show the quote to the user, and get explicit confirmation before executing without `--dry-run`.

### Swap Output Examples

**Quote output:**

```json
{
  "event": "swap_quote",
  "dryRun": true,
  "direction": "BTC_TO_USD",
  "preBalance": {
    "btcWalletId": "abc123",
    "usdWalletId": "def456",
    "btcBalanceSats": 50000,
    "usdBalanceCents": 1500,
    "usdBalanceFormatted": "$15.00"
  },
  "quote": {
    "quoteId": "blink-swap-1709424000-123456",
    "direction": "BTC_TO_USD",
    "requestedAmount": { "value": 1000, "unit": "sats" },
    "amountIn": { "value": 1000, "unit": "sats" },
    "amountOut": { "value": 68, "unit": "cents" },
    "feeSats": 0,
    "feeBps": 0,
    "rateSnapshot": { "satsPerDollar": 1470 },
    "executionPath": "blink:intraLedgerPaymentSend"
  }
}
```

**Execution output:**

```json
{
  "event": "swap_execution",
  "dryRun": false,
  "direction": "BTC_TO_USD",
  "status": "SUCCESS",
  "succeeded": true,
  "preBalance": { "btcBalanceSats": 50000, "usdBalanceCents": 1500 },
  "postBalance": { "btcBalanceSats": 49000, "usdBalanceCents": 1567 },
  "balanceDelta": { "btcDeltaSats": -1000, "usdDeltaCents": 67 },
  "execution": {
    "path": "blink:intraLedgerPaymentSend",
    "transactionId": "tx_abc123"
  }
}
```

## L402 Client Commands

L402 is an HTTP payment protocol: a server returns HTTP 402 with a Lightning invoice, the client pays, and retries the request with a proof-of-payment token. This skill can act as an L402 client.

Supports two L402 formats:

- **Lightning Labs** — `WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."`
- **l402-protocol.org** — JSON body with `payment_request_url` and `offers` array

### Discover L402 Pricing (no payment)

```bash
blink l402-discover <url> [--method GET|POST] [--header key:value]
```

Probes a URL for L402 payment requirements without paying. Returns the detected format, invoice, and decoded satoshi amount.

- `url` — the URL to probe (required)
- `--method GET|POST` — HTTP method to use (default: GET)
- `--header key:value` — extra request header (repeatable)

**No API key required for discovery.**

Known public L402 endpoints for testing (use specific paths, not root URLs; re-verified live in field test FT7, 2026-11-04):

- `https://api.lightningenable.com/l402/test/ping` — Lightning Labs format, **1 sat**, returns a fixed success message and accepts its token again (the reliable test endpoint). Other paid endpoints live under `https://api.lightningenable.com/l402/proxy/…` (about 2 sats); check each one's required query parameters first, since a missing parameter fails *after* payment. The old `lightningenable.com/api/v1/endpoint/<id>` pattern now returns 404.
- `https://www.l402apps.com/api/apis` — L402 API directory, 10 sats, Lightning Labs format. **Unreliable:** it returned HTTP 500 (`Failed to create Lightning invoice`) throughout FT7.

> Upstream availability shifts: `l402.services` (dead as of 2026-09-12) and `l402.directory` (intermittent 503 during rebuilds) have both been unreachable at times — `l402-search --source 402index` is the reliable directory fallback. Probe with `l402-discover` before relying on any endpoint.

### Pay for an L402-Gated Resource

```bash
blink l402-pay <url> [options]
```

Makes an HTTP request. If the server returns 402, automatically parses the challenge, pays the invoice, caches the token, and retries with the payment proof. Two payment backends:

- **custodial (default)** — the invoice is paid via the Blink API (`lnInvoicePaymentSend`); requires `BLINK_API_KEY` with Write scope.
- **spark** — the invoice is paid from the self-custodial (Spark) wallet via the Breez SDK (signs locally with the seed); requires `SPARK_MNEMONIC` + `BREEZ_API_KEY`, **no Blink API key**. The preimage comes back in the settled payment's HTLC details.

Both backends share the same budget reservation/enforcement, token cache, and retry flow, and the output carries a `backend` field.

- `url` — URL to access (required)
- `--wallet BTC|USD` — wallet to pay from (default: BTC; custodial backend only)
- `--spark` — pay from the self-custodial (Spark) wallet via the Breez SDK (BTC only). Auto-selected when no `BLINK_API_KEY` is set but `SPARK_MNEMONIC` is present
- `--max-amount <sats>` — refuse to pay more than N sats (safety limit)
- `--dry-run` — discover price without paying; always bypasses the token cache so the current invoice price is always shown even if a cached token exists; uses the same conservative charge as real execution
- `--method GET|POST|PUT|DELETE|PATCH` — HTTP method (default: GET)
- `--header key:value` — extra request header (repeatable)
- `--wait <seconds>` — Spark only: how long to poll an async (PENDING) settlement before failing (default 60; `0` disables). Spark settlement is asynchronous — a PENDING payment routinely settles seconds later carrying the preimage (the L402 token material), so the default waits rather than aborts. A timeout means the sats were spent but no token was captured: the error names the payment id (check `spark-transactions` before retrying — a retry pays again).
- `--body <string>` — request body for POST/PUT
- `--no-store` — disable token cache (do not read or write `~/.blink/l402-tokens.json`). It applies to **this run only**: if a request after payment fails, that payment's token is gone (re-running pays again). And if the server later re-issues the **same** already-paid invoice, a run *without* `--no-store` recovers that preimage from your transaction history and caches it.
- `--force` — pay even if a valid cached token exists
- `--probe` — estimate the routing fee before paying; warns and continues if the probe fails; adds a `feeProbe` field to the `l402_paid` output (custodial: `lnInvoiceFeeProbe`; spark: the prepare step always resolves the fee, so `--probe` is a no-op there). With `--dry-run` (v3.0.2) it also runs, without paying, and adds `feeProbe` to `l402_dry_run` (custodial only, needs `BLINK_API_KEY`; for `--spark`, use `blink spark-fee-probe <invoice> <amount>`). **The probe is an estimate, and its accuracy depends on the backend:** in the field tests the **custodial** probe estimated 1 sat while the actual routing fee was 10 sats on a 1–2 sat invoice (FT7), whereas the **Spark** probe matched exactly (3 sats, FT8). Neither budgets nor `--max-amount` count the fee, so for tiny invoices the fee can be several times the price.

**Requires Write scope on the API key (custodial backend) or `SPARK_MNEMONIC` + `BREEZ_API_KEY` (spark backend).**

> **AGENT:** Always run with `--dry-run` first to show the satoshi cost to the user. Confirm the amount and target URL before executing without `--dry-run`.

### Manage Token Cache

```bash
blink l402-store list
blink l402-store get <url|key>
blink l402-store clear [--expired]
```

- `list` — show all cached tokens (masks preimage for security)
- `get <url|key>` — retrieve the full token for a paid URL (normalized to its key) or a raw store key
- `clear` — remove all cached tokens
- `clear --expired` — remove only expired tokens

Token cache location: `~/.blink/l402-tokens.json`

**Origin isolation (v3.0.1):** tokens are keyed by the **origin** (scheme + host + port) + path of the URL that **actually issued the 402**, e.g. `https://api.example.com/v1/data`, and a cached token is only ever sent directly back to that URL. That is not necessarily the URL you passed: if a service redirects the request (even only for some methods, e.g. it answers `HEAD` itself but redirects `GET`), the token belongs to the redirect target, and `l402_paid` reports it as `challengeUrl`. Operator `--header`s are withheld from a different issuing origin, and a `--body` request whose 402 came from a different origin is refused (`URL_POLICY`) before paying. The credentialed retry repeats **exactly the request that received the 402** (same method, headers and body) with the L402 `Authorization` added, and is never rebuilt from your original flags. That includes HTTP redirect rewrites: 301/302 turn `POST` into `GET`, and 303 turns any non-`GET`/`HEAD` method into `GET`. It also covers header state along the chain: once a redirect leaves the origin, your `--header`s are dropped for the rest of the chain, even if it comes back, and a rewrite that drops the body also drops its `Content-Type`. An operator `--header Authorization` is never sent with the paid credential; the L402 token replaces it, with a warning on stderr. If such a rewrite **drops your `--body`**, the request is refused (`URL_POLICY`) before paying, on any origin, because the challenged request is no longer the one you invoked. Call the issuing URL directly instead. A 307/308 keeps the method and body, so those work as before. Each run first makes one credential-free request to learn which URL issues the challenge, so cache reuse costs one extra round trip. Before v3.0.1 the key was host + path, so a token could be replayed to a different service on another port of the same host. (Replay from `https` to plaintext `http` was possible only for local hosts such as `127.0.0.1`/`localhost`, or before v2.6.1: since v2.6.1 the URL guard refuses plaintext `http` to any other host before sending anything.) Entries written by older versions have no scheme; `list` flags them `legacy: true` and they are **never reused** (the next request pays fresh). Run `blink l402-store clear` to remove them.

**Server-set expiry is honored (v3.0.3).** Many L402 services put an expiry in the macaroon itself, e.g. `expires = <unix>` (FT8: lightningenable tokens last about an hour). The cache now reads that caveat (`expires=` or `<service>_valid_until=`), when saving and for entries cached before v3.0.3, and treats an expired token as absent. The next request pays for a fresh token (still subject to budget and allowlist) instead of replaying a stale one and getting a 402. `l402-store list` shows these tokens as `expired: true`, and `clear --expired` removes them.

**Failures after a credential is sent always emit JSON (v3.0.2).** If the request carrying the L402 credential dies before a response arrives (FT7: `terminated`, caused by a server's undecodable compressed reply), `l402-pay` exits 1 with:
- `l402_paid_retry_failed` — the payment **settled** but the paid retry failed. Includes `paymentStatus`, `paymentHash`, `satoshis`, `tokenStored`, `error`, and `errorCode` when the failure was a policy refusal (`URL_POLICY`, e.g. the credentialed response redirected to a host outside the allowlist). With `tokenStored: true`, re-running the same command retries with the cached token without paying again; with `tokenStored: false` (`--no-store`, a placeholder preimage, or a failed cache write), re-running pays again.
- `l402_reuse_failed` — a cached token was sent and the request failed (transport or `URL_POLICY`, reported in `errorCode`); **no payment was made**. Re-run to retry, or pass `--force` to pay fresh.

Before v3.0.2 both cases printed only `Error: …` on stderr with nothing on stdout.

**Placeholder preimages are never cached (v3.0.2).** If the Blink API returns no preimage and no payment hash, `l402-pay` still retries with a placeholder (which only non-strict servers accept) and reports `preimagePlaceholder: true`, but it no longer caches that token: a fabricated preimage is not a proof of payment.

### L402 Output Examples

**l402-discover (Lightning Labs format):**

```json
{
  "url": "https://api.example.com/resource",
  "l402_detected": true,
  "format": "lightning-labs",
  "macaroon": "AgELZXhhbXBsZS...",
  "invoice": "lnbc1000n1...",
  "satoshis": 100,
  "satoshisFormatted": "100 sats"
}
```

**l402-pay (dry-run):**

```json
{
  "event": "l402_dry_run",
  "url": "https://api.example.com/resource",
  "format": "lightning-labs",
  "invoice": "lnbc1000n1...",
  "satoshis": 100,
  "satoshisFormatted": "100 sats",
  "maxAmount": 1000,
  "withinBudget": true,
  "message": "Dry-run: would pay this invoice to access the resource. No payment made."
}
```

**l402-pay (after payment):**

```json
{
  "event": "l402_paid",
  "url": "https://api.example.com/resource",
  "format": "lightning-labs",
  "paymentStatus": "SUCCESS",
  "walletId": "abc123",
  "walletCurrency": "BTC",
  "satoshis": 100,
  "tokenReused": false,
  "retryStatus": 200,
  "data": { "...": "response from the protected resource" }
}
```

**l402-pay (after payment, with --probe):**

```json
{
  "event": "l402_paid",
  "url": "https://api.example.com/resource",
  "format": "lightning-labs",
  "paymentStatus": "SUCCESS",
  "walletId": "abc123",
  "walletCurrency": "BTC",
  "satoshis": 100,
  "tokenReused": false,
  "retryStatus": 200,
  "feeProbe": {
    "estimatedFeeSats": 1,
    "error": null
  },
  "data": { "...": "response from the protected resource" }
}
```

## L402 Producer Commands

L402 producer tools let you **protect your own API resources** behind a Lightning paywall. Issue challenges to clients, then verify their payment proofs before granting access.

Two-step workflow:

1. When a client requests a resource, call `blink l402-challenge` to create a signed payment challenge and return it with HTTP 402.
2. When the client submits a payment token, call `blink l402-verify` to verify the preimage and macaroon signature.

> **Note:** End-to-end round-trip testing (challenge → pay → verify) requires **two separate Blink accounts**. Blink does not allow paying your own invoice (CANT_PAY_SELF). Use a second account or wallet to pay the challenge invoice during testing.

### Create an L402 Challenge

```bash
blink l402-challenge --amount <sats> [options]
```

Creates a Lightning invoice via Blink and issues a signed macaroon bound to its payment hash. Returns a ready-to-send `WWW-Authenticate` header.

- `--amount <sats>` — invoice amount in satoshis (required)
- `--wallet <id>` — Blink BTC wallet ID (auto-resolved if omitted)
- `--memo <text>` — invoice memo / description
- `--expiry <seconds>` — macaroon caveat expiry (e.g. `3600` = 1 hour); controls how long the challenge is valid, not the invoice expiry. **Recommended:** without it the token **never expires** (`expiresAt: null`), so a paid token grants access indefinitely. Set an expiry that matches what you are selling.
- `--resource <id>` — resource identifier caveat (e.g. `/api/v1/data`); returned tokens will only be valid for this exact path

**Requires Write scope on the API key.**

Root key for HMAC signing resolves in this order:

1. `BLINK_L402_ROOT_KEY` env var (64-char hex, 32 bytes)
2. `~/.blink/l402-root-key` (auto-created on first run)

> **AGENT:** Keep `BLINK_L402_ROOT_KEY` or `~/.blink/l402-root-key` stable across server restarts. A different root key will invalidate all previously issued macaroons.

### Verify an L402 Payment Token

```bash
blink l402-verify --token <macaroon>:<preimage> [options]
blink l402-verify --macaroon <b64> --preimage <hex> [options]
```

Verifies a client-submitted L402 `Authorization` token. Performs three layers of verification:

1. **Preimage check:** `SHA-256(preimage) === payment_hash` — cryptographic proof the invoice was paid
2. **Signature check:** HMAC-SHA256 of macaroon body — proves the macaroon was issued by this server
3. **Caveat check:** expiry not exceeded, resource matches if constrained

- `--token <macaroon>:<preimage>` — L402 authorization token (colon-separated, from `Authorization: L402 <token>` header)
- `--macaroon <b64>` — base64url-encoded macaroon (alternative to `--token`)
- `--preimage <hex>` — 64-char hex preimage (alternative to `--token`)
- `--resource <id>` — expected resource identifier to check against the macaroon's resource caveat. **Required for a resource-scoped token (v3.0.2):** verifying one without `--resource` returns `valid: false` with `resourceUnchecked: true` (exit 1). Before v3.0.2 the caveat was silently skipped, so a token sold for one path was accepted for any request. Always pass the path of the request you are authorizing.
- `--check-api` — additionally query the Blink API to confirm PAID status (belt-and-suspenders)

Exit code `0` when `valid: true`, exit code `1` when `valid: false` or on error.

> **Note:** The `--preimage` value must be a 64-character hex string (32 bytes). Passing a plain string like `fake_preimage` will produce an error explaining the format requirement. For testing rejection, use a valid-format but wrong preimage: 64 zeros (`0000...0000`).

### L402 Producer Output Examples

**l402-challenge:**

```json
{
  "header": "L402 macaroon=\"AgEL...\", invoice=\"lnbc100n1...\"",
  "macaroon": "AgEL...",
  "invoice": "lnbc100n1...",
  "paymentHash": "abc123...64hex",
  "satoshis": 100,
  "expiresAt": 1735689600,
  "resource": "/api/v1/data"
}
```

Return this to clients as:

```
HTTP/1.1 402 Payment Required
WWW-Authenticate: L402 macaroon="AgEL...", invoice="lnbc100n1..."
```

**l402-verify (valid payment):**

```json
{
  "valid": true,
  "preimageValid": true,
  "signatureValid": true,
  "caveatsValid": true,
  "paymentHash": "abc123...64hex",
  "resource": "/api/v1/data",
  "expiresAt": 1735689600,
  "expired": false,
  "apiStatus": "NOT_CHECKED"
}
```

**l402-verify (invalid — wrong preimage):**

```json
{
  "valid": false,
  "preimageValid": false,
  "signatureValid": true,
  "caveatsValid": true,
  "paymentHash": "abc123...64hex",
  "resource": null,
  "expiresAt": null,
  "expired": false,
  "apiStatus": "NOT_CHECKED"
}
```

## L402 Service Discovery

Find L402-gated APIs that agents can pay for and access. Two directory sources:

- **l402.directory** (default) — curated registry with rich endpoint schemas, pricing, and consumption instructions
- **402index.io** — broader coverage (50+ services), simpler flat schema

### Search Services

```bash
blink l402-search                              # all live services from l402.directory
blink l402-search video                        # keyword search
blink l402-search --category data              # filter by category
blink l402-search --status all                 # include offline/new services
blink l402-search --format minimal             # compact output
blink l402-search ai --source 402index         # search 402index.io instead
```

**No API key required** — both directories have free browse APIs.

> **AGENT:** Use `l402-search` to find services before using `l402-pay`. Check pricing in the results before paying.

### Get Service Details

```bash
blink l402-info <service_id>                   # full details (free, l402.directory)
blink l402-info <service_id> --report          # paid health report (10 sats via L402)
blink l402-info <service_id> --report --force  # pay fresh, ignore cached token
```

- Without `--report`: free, returns endpoints, pricing, consumption instructions
- With `--report`: 10 sats, returns uptime percentages, probe history, response times
- `--report` is subject to budget controls and domain allowlist (domain: `l402.directory`)

### Discovery Output Example

```json
{
  "source": "l402.directory",
  "query": "video",
  "count": 1,
  "services": [
    {
      "service_id": "71adb942293c89f6",
      "name": "Hyperdope Video",
      "description": "Lightning-gated video streaming...",
      "status": "live",
      "categories": ["video", "streaming"],
      "endpoints": [
        {
          "url": "https://hyperdope.com/api/l402/videos/{hash}/master.m3u8",
          "method": "GET",
          "pricing": { "amount": 10, "currency": "sats", "model": "per-request" }
        }
      ]
    }
  ]
}
```

## Budget Controls

Prevent runaway spending in autonomous agent workflows with rolling spend limits and domain allowlist.

### Configuration

Env vars take precedence over the config file (`~/.blink/budget.json`):

| Env var                      | Config file key   | Default         | Description                                                                               |
| ---------------------------- | ----------------- | --------------- | ----------------------------------------------------------------------------------------- |
| `BLINK_BUDGET_HOURLY_SATS`   | `hourlyLimitSats` | none            | Max sats in rolling 1-hour window                                                         |
| `BLINK_BUDGET_DAILY_SATS`    | `dailyLimitSats`  | none            | Max sats in rolling 24-hour window                                                        |
| `BLINK_L402_ALLOWED_DOMAINS` | `allowlist`       | none (deny all) | Comma-separated domains for L402 auto-pay — empty/unset denies every domain (fail-closed) |

**Unconfigured means "deny" for autonomous spending, not "unlimited".** The two
kinds of payment behave differently on purpose:

> **Security (v2.6.1):** the allowlist now gates **every non-dry-run `l402-pay` outbound request** (pre-flight, before canonicalization/probing), not only the payment itself — when an allowlist is configured, a URL outside it is refused before a single byte leaves the machine. All L402 fetches (`l402-pay`, `l402-discover`, and the server-supplied l402-protocol `payment_request_url`) route through the shared SSRF guard: private/loopback/link-local/metadata targets refused (incl. IPv4-mapped IPv6), redirects followed manually and re-validated per hop. `l402-discover` remains the ungated-but-guarded public prober; `l402-pay --dry-run` likewise (enforced since v3.0.2; before that, a configured allowlist wrongly gated both). State files under `~/.blink` are `0700`/`0600` with atomic writes and symlink refusal (macaroons + preimages are a reusable bearer credential pair; since v3.0.2 the producer signing key `~/.blink/l402-root-key` is covered too).

- **Explicit one-shot payments** — `pay-invoice`, `pay-lnaddress`, `pay-lnurl`,
  `spark-send`. You chose the recipient and amount, so these run with or
  without a budget. If limits are configured they are enforced; if not, the
  payment proceeds.
- **Autonomous L402 auto-pay** — `l402-pay`, and `l402-info --report` which
  delegates to it. These spend without a human in the loop for each payment, so
  they **fail closed**: with no budget configured, or an empty domain
  allowlist, the payment is refused. Configure both before enabling auto-pay.

### Budget Commands

```bash
blink budget status                              # Show current spend vs limits
blink budget set --hourly 1000 --daily 5000      # Set spending limits
blink budget set --off                           # Remove all limits
blink budget log [--last 10]                     # Show recent spending entries
blink budget reset                               # Clear finalized history (keeps active reservations)
blink budget reset --force                       # Clear EVERYTHING incl. reservations — unsafe mid-payment
blink budget allowlist list                      # Show allowed L402 domains
blink budget allowlist add satring.com           # Add domain to allowlist
blink budget allowlist remove satring.com        # Remove domain from allowlist
```

**Allowlist matching is exact-host:** `lightningenable.com` does **not** cover `www.lightningenable.com` or `api.lightningenable.com`; add each host you pay. The allowlist is a **payment** policy: it gates every non-dry-run `l402-pay` request, while `l402-discover` and `l402-pay --dry-run` stay ungated public probes. For them the list can only *permit* a listed private/local host, and **only when that is the host you passed**: a redirect or a server-supplied `payment_request_url` that points at a listed private host from anywhere else is refused, so a public server can never use your allowlist entry to reach a local service. Every request by **name** is also refused when the name **resolves** to a private, loopback, link-local or metadata address (e.g. `ip6-localhost`, or attacker DNS like `127.0.0.1.nip.io`), in every mode including no allowlist. A name whose address **cannot be verified** (DNS error, timeout, empty answer) is refused too, never fetched (fail closed). To reach a LAN service by name, add that host to the allowlist. DNS rebinding after a verified public answer remains a known limit (see [non-custodial](references/non-custodial.md)). Before v3.0.2 a configured allowlist wrongly blocked both probes. (For real payments the list stays exclusive: every host on it is one you chose to allow.)

### Budget Status Output Example

```json
{
  "enabled": true,
  "hourlyLimit": 1000,
  "dailyLimit": 5000,
  "hourlySpent": 350,
  "dailySpent": 1200,
  "hourlyRemaining": 650,
  "dailyRemaining": 3800,
  "effectiveRemaining": 650,
  "allowlist": ["satring.com", "l402.services"],
  "logEntries": 8
}
```

> **The rolling windows are absolute across sessions.** `dailySpent` counts
> every logged spend from the last 24 hours — including those made by
> previous CLI runs — so a freshly set tight limit can refuse a small payment
> for reasons that look like a defect. Check `dailySpent` before setting low
> test caps (observed live, FT4: `--daily 100` refused a 1-sat l402 payment
> because the prior session's spends were still in-window).

`effectiveRemaining` = min(hourlyRemaining, dailyRemaining) — the actual amount the agent can spend right now.

### How Budget Enforcement Works

- **Checked before every outbound payment:** `pay-invoice`, `pay-lnaddress`, `pay-lnurl`, `l402-pay`, `spark-send` (after fee resolution, before signing)
- **Reserved, not just checked:** the amount is **reserved** under the budget lock before the payment executes, then finalized (success/pending) or released (known failure) — two concurrent payments can never both pass the same remaining budget. **Outcome-unknown errors after dispatch** (timeout, lost response) keep the reservation in place: the payment may still settle, so the budget stays blocked until the 25h prune. A crash between payment and finalization behaves the same; reserved entries appear in `budget log` with `"state": "reserved"`.
- **Principal only:** budgets count the payment amount, not the routing fee — for the custodial commands and `spark-send` alike. Invoice amounts are charged **ceil with a 1-sat minimum for any positive decodable amount** (a 1400-msat invoice charges 2 sats; a 500-msat invoice charges 1 sat — explicit payments can never move funds untracked). `l402-pay` additionally refuses invoices below 1 satoshi entirely; its dry-run preview uses the exact same charge as execution.
- **Unconfigured budget:** allowed for explicit one-shot payments; **denied** for `l402-pay` auto-pay
- **Domain allowlist:** checked for `l402-pay` only — an empty allowlist blocks all auto-pay
- **Fail closed for auto-pay:** `l402-pay` refuses to run unless a budget AND a non-empty domain allowlist are explicitly configured (`NO_BUDGET_CONFIGURED` / `NO_ALLOWLIST_CONFIGURED` errors explain the setup)
- **`--force` never bypasses these checks:** on `l402-pay` it forces a fresh payment instead of reusing a cached token; budget and allowlist still apply. On `spark-send` it is the explicit opt-out for an over-limit one-shot send.
- **`--dry-run` shows budget impact:** dry-run output includes a `budget` field showing remaining budget (dry-run never pays, so it works without configuration)
- **Spending recorded after success:** only successful/pending payments are logged
- **Auto-pruning:** log entries older than 25 hours are removed automatically
- **`budget reset` and in-flight reservations:** an ordinary reset clears finalized history but **keeps active reservations**, so a payment in flight never reopens its allowance window. `budget reset --force` clears everything (the escape hatch for wedged reservations); if a force-cleared payment later completes, its spend is re-recorded — but the freed allowance can briefly be reused, so never force-reset while payments are in flight.
- **Lock recovery:** budget mutations hold a lockfile at `~/.blink/.spending-log.lock` (max a few seconds each). If a crashed process leaves it behind, commands time out with a `BUDGET_LOCK_TIMEOUT` error — remove the file manually; automatic stale takeover is deliberately not attempted.
- **Corrupt log fails closed:** if the spending log can't be read or parsed, budget checks and payments throw `BUDGET_LOG_CORRUPT` — prior spend is unknown and is never treated as zero, and the damaged file is never overwritten. Recover with `blink budget reset --force` (discards it) or fix/remove the file manually.
- **Corrupt config fails closed too:** a damaged `~/.blink/budget.json` throws `BUDGET_CONFIG_CORRUPT` rather than silently dropping your limits; a garbage limit env var (e.g. `BLINK_BUDGET_DAILY_SATS=abc`) throws `BUDGET_ENV_INVALID` naming the variable instead of being treated as unset. Recover by fixing or removing the file, then re-run `blink budget set`. Options are scoped per subcommand — `budget status --force` errors instead of being ignored.

> **AGENT:** Before making a payment, check budget status with `blink budget status` to see remaining budget. If budget is exceeded, inform the user and suggest increasing limits with `blink budget set`.

## Security

### API Key Handling

- **Your API key is your wallet access** — anyone with a Write-scoped key can spend your entire balance.
- **Use minimum scopes** — Read-only for balance checks, Receive for invoices, Write only when sending.
- **Never expose keys in output** — do not echo, log, or include `BLINK_API_KEY` in chat messages or files.
- Keys are for server-side / agent use only. Never embed in client-side code.

### What Data Leaves the Machine

- **Outbound HTTPS** to `api.blink.sv` (or `BLINK_API_URL` override) for all GraphQL queries and mutations.
- **Outbound WSS** to `ws.blink.sv` (or `BLINK_WS_URL` override) for subscription WebSockets.
- **L402 requests** go directly to the third-party URL you provide to `l402-discover` or `l402-pay`. The Blink API is contacted only when a payment is needed.
- **LNURL receive** (`resolve-receiver`, `create-invoice-lnaddress`) contacts the Blink API host (`BLINK_API_URL`) for an **unauthenticated `accountDefaultWallet` classification probe**, then `blink.sv` and its LNURL service host `lnurl.blink.sv` — all allowlisted, every redirect re-validated. A transport/5xx failure of the probe aborts (`CUSTODIAL_PROBE_FAILED`) rather than assuming the recipient is non-custodial; only an authoritative "no such custodial account" answer falls through to LNURL. Blocking the GraphQL host therefore breaks both credential-free commands.
- **`spark-*` commands and `l402-pay --spark`** additionally contact Breez/Spark infrastructure (authenticated with `BREEZ_API_KEY`). `l402-pay --spark` contacts the target resource's host (any URL you provide) plus Breez/Spark for the payment. `spark-send` and `spark-fee-probe` with a Lightning Address or LNURL destination also contact the **recipient's LNURL service** — the address domain and its callback host — during SDK parse/prepare. Note this happens _before_ a configured budget can reject an over-limit send. Signing happens locally; the seed never leaves the machine.
- **No other network calls** beyond those listed here. Scripts do not phone home, send telemetry, or contact any undisclosed third-party services.

### Filesystem Access

- **Credential handling:** `BLINK_API_KEY` is read from `process.env` only. Shell rc files are never read, and no credential is ever written outside the process.
- **QR PNG generation:** The `qr` command (and `--qr`) writes each PNG into a fresh private directory, `<system temp>/blink-qr-XXXXXX/invoice.png` (directory `0700`, file `0600`, created exclusively). Before v3.0.5 it wrote to a predictable `/tmp/blink_qr_<timestamp>.png`, which another local user could redirect with a planted symlink (ClawHub 3.0.4 ClawScan). These are standard image files with no embedded metadata beyond the QR content.
- **L402 token cache:** The `l402-pay` command writes paid tokens to `~/.blink/l402-tokens.json`. This file contains macaroons and preimages for previously-paid L402 services. Use `blink l402-store clear` to remove all cached tokens. Pass `--no-store` to disable caching entirely.
- **Budget files:** Budget config at `~/.blink/budget.json` and spending log at `~/.blink/spending-log.json`. The spending log is auto-pruned (entries older than 25h removed). Use `blink budget reset` to clear the log.
- **Spark SDK state:** `spark-*` commands and `l402-pay --spark` write Breez SDK wallet state to `~/.blink/spark/<network>-<hash>` (the directory name is a non-reversible sha256 prefix of the seed). Delete the directory to remove all local state.

### Stateless Design

Most scripts are stateless. Exceptions:

- `l402-pay` maintains a token cache at `~/.blink/l402-tokens.json` to avoid re-paying for previously-accessed L402 services. Use `--no-store` to run without any persistence.
- All payment commands (`pay-invoice`, `pay-lnaddress`, `pay-lnurl`, `l402-pay`, `spark-send`) log spending to `~/.blink/spending-log.json` for budget enforcement. This log is auto-pruned and can be cleared with `blink budget reset`.
- `spark-*` commands persist Breez SDK wallet state at `~/.blink/spark/<network>-<hash>`. Deleting that directory resets local state (funds live on Spark; the seed restores the wallet).

### Payment Safety

- **Sending is irreversible** — Lightning payments cannot be reversed once settled.
- **Test on staging first** — use `BLINK_API_URL=https://api.staging.blink.sv/graphql` to point at the signet staging environment with test funds.
- **USD invoices expire fast** — ~5 minutes due to exchange rate lock.
- **Price queries are public** — `blink price` works without an API key; only wallet operations require authentication.
- **L402 preimage resolution** — After payment, `l402-pay` retrieves the preimage inline from the mutation response (`settlementVia.preImage`). If the inline preimage is unavailable (e.g. race condition or network issue), it falls back to a `transactions` query matched by payment hash. If the transaction is not yet indexed, it falls back to a SHA-256(invoice) placeholder, which works with servers using token-based verification but may fail with servers that cryptographically verify the preimage against the payment hash.

## Reference Files

- [blink-api-and-auth](references/blink-api-and-auth.md): API endpoints, authentication, scopes, staging/testnet configuration, and error handling.
- [payment-operations](references/payment-operations.md): send workflows, BTC vs USD wallet selection, fee probing, and safety guardrails.
- [invoice-lifecycle](references/invoice-lifecycle.md): invoice creation, two-phase output parsing, monitoring strategies, QR generation, and expiration handling.
- [swap-operations](references/swap-operations.md): BTC <-> USD internal conversion, quote/execute workflow, rounding behavior, and effective cost formulas.
- [non-custodial](references/non-custodial.md): non-custodial (Spark) accounts — credential-free receiving via LNURL-pay, seed-gated `spark-*` commands, Breez API key setup, SSRF guard, and seed security model.
- [Blink Agent Playbook](https://dev.blink.sv/api/agent-playbook): Canonical AI agent API reference — order of operations, safety constraints, and verification checklist.
- [llms.txt](https://dev.blink.sv/llms.txt): Machine-readable discovery metadata for AI agents (endpoints, source URLs, hard rules).

## Files

- `{baseDir}/scripts/balance.js` — Check wallet balances
- `{baseDir}/scripts/create_invoice.js` — Create BTC Lightning invoices (auto-subscribes to payment status)
- `{baseDir}/scripts/create_invoice_usd.js` — Create USD-denominated Lightning invoices (auto-subscribes to payment status)
- `{baseDir}/scripts/check_invoice.js` — Check invoice payment status (polling)
- `{baseDir}/scripts/pay_invoice.js` — Pay BOLT-11 invoices (BTC or USD wallet)
- `{baseDir}/scripts/pay_lnaddress.js` — Pay to Lightning Addresses (BTC or USD wallet)
- `{baseDir}/scripts/pay_lnurl.js` — Pay to LNURL strings (BTC or USD wallet)
- `{baseDir}/scripts/fee_probe.js` — Estimate payment fees (BTC or USD wallet)
- `{baseDir}/scripts/qr_invoice.js` — Render invoice QR code (terminal + PNG file)
- `{baseDir}/scripts/transactions.js` — List transaction history
- `{baseDir}/scripts/price.js` — Get BTC/USD exchange rate
- `{baseDir}/scripts/account_info.js` — Show account info and limits
- `{baseDir}/scripts/subscribe_invoice.js` — Subscribe to invoice payment status (standalone)
- `{baseDir}/scripts/subscribe_updates.js` — Subscribe to realtime account updates
- `{baseDir}/scripts/_swap_common.js` — Shared swap helpers (quote estimation, execution, wallet pair management)
- `{baseDir}/scripts/swap_quote.js` — Get BTC <-> USD conversion quote
- `{baseDir}/scripts/swap_execute.js` — Execute BTC <-> USD wallet conversion
- `{baseDir}/scripts/l402_discover.js` — Probe a URL for L402 payment requirements (no payment)
- `{baseDir}/scripts/l402_pay.js` — Auto-pay L402-gated resources via Blink + token caching
- `{baseDir}/scripts/l402_store.js` — Manage the L402 token cache (~/.blink/l402-tokens.json)
- `{baseDir}/scripts/_l402_macaroon.js` — Shared macaroon module: encode/decode/sign/verify + root key management
- `{baseDir}/scripts/l402_challenge_create.js` — Create L402 payment challenges (invoice + signed macaroon)
- `{baseDir}/scripts/l402_payment_verify.js` — Verify L402 client payment tokens (preimage + HMAC + caveats)
- `{baseDir}/scripts/l402_search.js` — Search L402 service directories (l402.directory, 402index.io)
- `{baseDir}/scripts/l402_info.js` — Get full L402 service details + paid health reports
- `{baseDir}/scripts/_budget.js` — Shared budget module: config resolution, spend log, rolling limits, domain allowlist
- `{baseDir}/scripts/budget.js` — Budget controls CLI (status, set, log, reset, allowlist)
- `{baseDir}/scripts/_lnurl.js` — Zero-dependency LNURL client (LUD-06/16/21) with SSRF host allowlisting
- `{baseDir}/scripts/_spark_sdk.js` — Shared Breez Spark SDK module: connect, seed validation, balance/payment normalization
- `{baseDir}/scripts/resolve_receiver.js` — Classify a Blink identifier as custodial or non-custodial (Spark)
- `{baseDir}/scripts/create_invoice_lnaddress.js` — Receive to any Blink Lightning Address via public LNURL-pay (no credentials)
- `{baseDir}/scripts/spark_balance.js` — Non-custodial (Spark) BTC balance via the SDK
- `{baseDir}/scripts/spark_info.js` — Non-custodial (Spark) account info via the SDK (getInfo dump)
- `{baseDir}/scripts/spark_send.js` — Sign & send from a Spark account (BOLT-11 / LNURL / Spark address)
- `{baseDir}/scripts/spark_fee_probe.js` — Estimate the fee / conversion quote to send from a Spark account (prepare only, nothing sent)
- `{baseDir}/scripts/spark_token_info.js` — Fetch BTKN token metadata (name, ticker, decimals)
- `{baseDir}/scripts/spark_receive_token.js` — Mint a Spark invoice to receive a BTKN token (e.g. USDB)
- `{baseDir}/scripts/spark_lnaddress.js` — Manage the wallet's @blink.sv Lightning address (get/check/register/delete)
- `{baseDir}/scripts/spark_transactions.js` — List Spark account payments (SDK-local history)
- `{baseDir}/scripts/spark_subscribe.js` — Stream live Spark wallet events
