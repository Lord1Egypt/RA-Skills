# Botwallet CLI

You are an expert at using the Botwallet CLI — the payment infrastructure that lets AI agents hold, spend, and earn USDC on Solana.

This skill covers everything you need to operate autonomously with money: creating wallets, making payments, earning through paylinks, accessing paid APIs via x402, requesting funds, withdrawing, and working within your human owner's guard rails.

---

## Core Concepts

### You Have a Human Owner

Every Botwallet wallet is tied to a human owner. They claim your wallet, fund it, set spending limits, and approve high-value transactions. You operate autonomously within the boundaries they set. When something exceeds those boundaries, it goes to them for approval.

The human manages everything through the **Human Portal** (dashboard at `app.botwallet.co`). There they can:
• See all their agents' wallets, balances, and activity
• Approve or reject payments, withdrawals, and x402 purchases
• Set guard rails: per-transaction limits, daily limits, merchant allowlists
• Fund wallets and respond to fund requests
• Claim wallets you create for them

### Two-Step Transaction Pattern

All transactions that move money follow the same two-step pattern:

1. **Create intent** — tells the server what you want to do. The server checks guard rails and returns a status.
2. **Confirm** — FROST threshold signs the transaction and submits it to Solana.

This applies to `pay`, `withdraw`, and `x402 fetch`. The pattern exists because of FROST signing — you hold key share S1, the server holds S2, and both must cooperate.

### FROST 2-of-2 Threshold Signing

Your wallet uses FROST (Flexible Round-Optimized Schnorr Threshold) signatures. During wallet creation, a Distributed Key Generation (DKG) ceremony produces two key shares:

• **S1** (yours): stored locally at `~/.botwallet/seeds/<wallet>.seed`
• **S2** (server): held by Botwallet, never sent to you

The full private key never exists anywhere. Every transaction requires both parties to produce partial signatures that combine into a valid Ed25519 signature. This is why the `confirm` step exists — it's the FROST signing ceremony.

### Output Format

The CLI outputs **JSON by default** (designed for you). Every response follows:
• Success: `{ "field": "value", ... }`
• Error: `{ "error": "CODE", "message": "...", "how_to_fix": "..." }`

The `--human` flag switches to colored, formatted output for human-readable display. As an agent, you should almost never need it.

### All Money Is USDC on Solana

Amounts are always in USDC (a dollar-pegged stablecoin on Solana). When you see `10.00`, that means $10.00 USDC.

---

## Getting Started

The setup flow should feel seamless — install, register, and onboard the human in one smooth sequence. Keep setup efficient and proceed through the steps smoothly.

### Step 1: Install the CLI

```bash
npm install -g @botwallet/agent-cli
```

Alternatively, if Go is available: `go install github.com/botwallet-co/agent-cli@latest`

#### Handling the PATH issue (important on Windows)

On Windows (and sometimes macOS/Linux), `npm install -g` installs the binary but the npm global bin directory may not be in PATH. The `botwallet` command will fail with "not recognized" or "command not found" even though installation succeeded.

**After installing, always verify the command is accessible:**

```bash
botwallet --help
```

**If that fails**, troubleshoot it:

1. Find the npm global prefix:
   ```bash
   npm prefix -g
   ```
2. The binary location depends on OS:
   - **Windows**: `<npm-prefix>\botwallet.cmd` (e.g., `C:\Users\<user>\AppData\Roaming\npm\botwallet.cmd`)
   - **macOS/Linux**: `<npm-prefix>/bin/botwallet`
3. Try running with the full path to confirm it works:
   ```bash
   # Windows example:
   "C:\Users\<user>\AppData\Roaming\npm\botwallet.cmd" --help
   ```
4. If the full path works, either:
   - **Add the npm global bin directory to PATH** for the current session so subsequent commands work normally. Use the output of `npm prefix -g` to construct the correct path for your OS.
   - **Or use the full path** for all subsequent `botwallet` commands in this session

The goal is a working `botwallet` command. Resolve the PATH issue and continue with registration.

### Step 2: Register a Wallet

#### Picking a name

The `--name` flag is required. **Pick a descriptive name** and suggest it to the human. Good names:

• **Use your own identity**: `"Claude's Wallet"`, `"GPT-4 Budget"`, `"Cursor Agent Wallet"`
• **Use the purpose**: `"Research Budget"`, `"x402 APIs Allowance"`, `"Dev Services Fund"`
• **Be creative**: `"Orion's Treasure Chest"`, `"The War Room Fund"`

The name is visible to the human when they claim the wallet, so make it recognizable. If you know the human's name or context, personalize it. Keep it under a few words.

#### Running register

```bash
botwallet register --name "<your chosen name>" --owner <human's email if known>
```

If you know the human's email, pass `--owner` — the wallet will appear in their portal automatically. If you don't know their email, register without it and set it later with `botwallet wallet owner <email>`.

You can optionally add metadata to help your human identify this wallet later. This is not required — registration works fine without it.

```bash
botwallet register --name "Research Assistant" --owner alice@co.com \
  --desc "Handles API calls for the ML research project" \
  --meta platform=cursor --meta project=ml-research
```

Suggested `--meta` keys: `platform`, `project`, `environment`, `hostname`. You can add any key that helps your human tell wallets apart.

The response includes:
• `claim_url` + `claim_code` — the human needs both to activate the wallet
• `next_step` — guidance on what to tell the human
• `on_claimed` — what to do after the human confirms claiming

### Step 3: Onboard the Human

After registration, immediately share the claim details with your human. Make it exciting — they're unlocking the ability to work with you financially. Include the claim link and code, explain what it means (invoices, payments, paid APIs, fund requests), and ask them to let you know once they've claimed it.

### Step 4: After Claiming — the Welcome Invoice

When the human confirms claiming, celebrate by creating a **sample invoice** with `botwallet paylink create`. Make it fun, personalized, and relevant:

```bash
botwallet paylink create --desc "Wallet Setup & First Invoice" \
  --item "Setting up your wallet, 1.00" \
  --item "Being an awesome agent, 3.00" \
  --item "Creating your first invoice, 1.00"
```

Then send it to the human:

```bash
botwallet paylink send <request_id> --to <human's email>
```

Explain that this is a sample invoice to demo how payments work. If they pay it, the money goes to the shared wallet (they can withdraw anytime for free). You can send real invoices to anyone, pay other agents, access paid APIs, and request funds. Keep it engaging and show real capabilities.

---

## Spending Money (Payments)

### Pay Another Agent or Merchant

```bash
botwallet pay @recipient 10.00                   # Step 1: create intent
botwallet pay confirm <transaction_id>           # Step 2: FROST sign & submit
```

Recipients can be `@username` (merchant or agent) or a raw Solana address. Always verify a recipient exists first with `botwallet lookup @username`.

### Pre-Check Before Paying

```bash
botwallet pay preview @recipient 10.00
```

This checks balance, fees, spending limits, and guard rails without creating a transaction. Use this to avoid failed attempts.

### Pay a Paylink

When another agent or merchant sends you a paylink:

```bash
botwallet pay --paylink pl_abc123
botwallet pay confirm <transaction_id>
```

### Useful Flags

• `--note "reason"` — visible to recipient
• `--reference "your-id"` — your internal tracking ID
• `--idempotency-key "key"` — prevents duplicate payments (use when retrying)

### What Happens After Step 1

The server checks guard rails and returns a status:

| Status | Meaning | What To Do |
|--------|---------|------------|
| `pre_approved` | Within limits, ready to go | Run `pay confirm` immediately |
| `awaiting_approval` | Exceeds limits or requires human OK | Tell your human, then poll `approval status <id>` |
| `approved` | Human approved it | Run `pay confirm` |
| `rejected` | Guard rails blocked it | Check `how_to_fix` in the response |

### Manage Payments

```bash
botwallet pay list                               # Actionable payments
botwallet pay list --status all                  # Full history
botwallet pay cancel <transaction_id>            # Cancel pending payment
```

---

## Earning Money (Paylinks)

Paylinks are how you get paid. Create a payment link, share it, and receive funds when someone pays.

### Create a Paylink

```bash
botwallet paylink create 25.00 --desc "Research report"
```

Returns a `payment_url` anyone can pay — agents use `botwallet pay --paylink <id>`, humans use the web interface.

### Create an Itemized Invoice

```bash
botwallet paylink create --desc "Dev services" \
  --item "API Calls, 5.00, 2" \
  --item "Setup Fee, 10.00"
```

Format: `--item "description, price[, quantity]"`. Quantity defaults to 1. Total is auto-calculated from items.

### Send a Paylink to Someone

```bash
botwallet paylink send <request_id> --to client@example.com          # Email
botwallet paylink send <request_id> --to @other-bot                  # Bot inbox
botwallet paylink send <request_id> --to @bot --message "Invoice"    # With note
```

### Track and Manage Paylinks

```bash
botwallet paylink get <paylink_id>               # Check if paid
botwallet paylink get --reference my-ref-123     # Look up by your reference
botwallet paylink list                           # List all paylinks
botwallet paylink list --status pending          # Filter by status
botwallet paylink cancel <paylink_id>            # Cancel pending paylink
```

Paylinks expire (default 24h, configurable with `--expires "7d"`). Monitor them.

---

## Accessing Paid APIs (x402)

The x402 protocol lets you pay for API calls using HTTP 402. You can browse available APIs, probe prices without paying ("window shopping"), and only pay when you're ready.

### Discover Available APIs

```bash
botwallet x402 discover                          # Curated, verified Solana APIs
botwallet x402 discover "weather"                # Search by keyword
botwallet x402 discover --bazaar                 # Full x402 Bazaar (Coinbase CDP)
botwallet x402 discover --bazaar --all           # Include non-Solana networks
```

The curated catalog contains APIs verified to work with Solana USDC. The Bazaar is the broader x402 ecosystem.

### Probe and Pay for an API

```bash
botwallet x402 fetch <url>                       # Step 1: probe (free = instant data)
botwallet x402 fetch confirm <fetch_id>          # Step 2: pay and get data
```

Step 1 makes an HTTP request without paying:
• If the API is free (200), you get the data immediately — no step 2 needed
• If the API requires payment (402), you see the price and get a `fetch_id`

You can probe multiple APIs to compare prices before committing. Guard rails apply to x402 purchases just like regular payments.

### POST/PUT Requests

```bash
botwallet x402 fetch https://api.example.com/query \
  --method POST \
  --body '{"q": "test"}' \
  --header "Accept: application/json"

botwallet x402 fetch confirm <fetch_id> \
  --method POST \
  --body '{"q": "test"}'
```

Pass the same `--method`, `--body`, and `--header` to both `fetch` and `fetch confirm` so the paid request matches.

---

## Requesting Funds

When you need more money, ask your human owner:

```bash
botwallet fund 50.00 --reason "API costs running low"
```

Always provide a clear reason — your owner sees this in their dashboard and decides whether to approve. Check the status:

```bash
botwallet fund list
botwallet fund list --status pending
```

---

## Withdrawals

Withdraw USDC to an external Solana address. All withdrawals require owner approval.

```bash
botwallet withdraw 50.00 <solana-address> --reason "Pay hosting"     # Step 1
# ... owner approves on dashboard ...
botwallet withdraw confirm <withdrawal_id>                            # Step 2
botwallet withdraw get <withdrawal_id>                                # Check status
```

---

## Guard Rails & Approvals

Your human owner sets guard rails that control what you can do autonomously:

• **Per-transaction limit** — max amount per single payment
• **Daily limit** — max total spending per day
• **Merchant allowlist** — restrict payments to approved recipients only

Check your current limits:

```bash
botwallet limits
```

### Handling Approvals

When a transaction needs human approval:

1. The command returns `awaiting_approval` with an `approval_id` and `approval_url`
2. Tell your human to approve at the `approval_url`
3. Poll until resolved:

```bash
botwallet approval status <approval_id>
```

Returns: `pending`, `approved`, `rejected`, or `expired`.

4. When `approved`, run the corresponding `confirm` command

**Important**: save the `approval_id` and `transaction_id` to persistent memory so you can check back later.

### Checking All Pending Approvals

```bash
botwallet approvals
```

---

## Events & Notifications

The events system is how you learn about asynchronous updates — approvals resolved, deposits received, payments completed.

```bash
botwallet events                                 # Unread events
botwallet events --type approval_resolved        # Filter by type
botwallet events --all                           # Include already-read
botwallet events --mark-read                     # Mark all as read
```

Event types you should care about:

| Event | Meaning |
|-------|---------|
| `approval_resolved` | Human approved/rejected a pending action |
| `deposit_received` | Funds arrived in your wallet |
| `payment_completed` | A payment you made settled on-chain |
| `fund_request_funded` | Human funded your request |
| `guardrails_updated` | Your spending limits changed |
| `x402_payment_completed` | x402 API payment succeeded |
| `x402_payment_failed` | x402 API payment failed |

### Heartbeat

Run `botwallet events` at the start of each session and periodically during long tasks. This is how you pick up approvals, deposits, and other updates that happened while you were idle.

```bash
botwallet events                                 # Check for unread events
```

When events come back, act on the actionable ones:

1. `approval_resolved` — the human responded to something you submitted. If the status is `approved`, run the corresponding `confirm` command (e.g., `botwallet pay confirm <transaction_id>` or `botwallet withdraw confirm <withdrawal_id>`). If `rejected`, note the reason and move on.
2. `fund_request_funded` — funds you requested have arrived. Run `botwallet wallet balance` to confirm, then continue with the task that needed funding.
3. `deposit_received` / `payment_completed` / `guardrails_updated` — informational. No action required.

After you've processed all events, clear the queue:

```bash
botwallet events --mark-read
```

Only run `--mark-read` after you've acted on everything. Once marked, events won't appear in future checks.

---

## Wallet Management

### Multiple Wallets

```bash
botwallet wallet list                            # See all local wallets
botwallet wallet use <name>                      # Switch default
botwallet wallet balance --wallet <name>         # Check specific wallet
```

### Wallet Info & Deposit

```bash
botwallet wallet info                            # Full wallet details + claim status
botwallet wallet balance                         # Balance and spending limits
botwallet wallet deposit                         # Solana USDC deposit address
```

### Backup & Portability

```bash
botwallet wallet backup                          # Start Key 1 backup (two-step)
botwallet wallet export -o wallet.bwlt           # Export encrypted wallet file
botwallet wallet import wallet.bwlt              # Import on another machine
```

### Change Owner (Unclaimed Wallets Only)

```bash
botwallet wallet owner new-human@example.com
```

### Rename Wallet

```bash
botwallet wallet rename "New Display Name"    # @username stays the same
```

---

## Error Handling

Every error response includes `error` (code), `message`, and `how_to_fix`. Common errors:

| Error Code | Meaning | Action |
|------------|---------|--------|
| `INSUFFICIENT_FUNDS` | Not enough balance | Use `fund ask` or check `wallet deposit` |
| `DAILY_LIMIT_EXCEEDED` | Over daily spending cap | Wait or ask owner to increase limit |
| `APPROVAL_REQUIRED` | Needs human sign-off | Share approval_url with owner |
| `WALLET_NOT_CLAIMED` | Wallet inactive | Tell human to claim it |
| `RECIPIENT_NOT_FOUND` | Invalid @username | Verify with `lookup` first |
| `NO_API_KEY` | Missing auth config | Set the `BOTWALLET_API_KEY` env var or pass `--api-key` |

---

## Configuration

Auth config is saved automatically on wallet creation:

• `~/.botwallet/config.json` — wallet registry, keys, default wallet
• `~/.botwallet/seeds/<wallet>.seed` — your key share (S1)

Auth resolution order:
1. `--api-key` flag
2. `BOTWALLET_API_KEY` env var
3. `--wallet` flag (selects from config)
4. Default wallet from config

---

## More Help

Every command has detailed help:

```bash
botwallet <command> --help                       # Command-specific help
botwallet docs                                   # Full embedded documentation
botwallet docs --json                            # Machine-readable command schema
```
