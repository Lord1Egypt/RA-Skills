---
name: aionmarket-trading
description: |
  Core trading skill for AION Market prediction market agents.
  Provides agent setup, wallet binding, market search, automated pre-trade
  checks, risk-aware trading, order management, position monitoring, and
  settlement workflows on Polymarket and Kalshi via the aion-sdk Python package.

  Use when: an AI agent needs to register, configure wallets, search markets,
  place or cancel trades, monitor positions, or run settlement-related flows on AION Market / Polymarket / Kalshi.
metadata:
  author: "AION Market"
  version: "0.3.0"
  homepage: "https://www.aionmarket.com/"
  docs: "https://docs.aionmarket.com/"
  sdk: "aion-sdk (PyPI)"
---

# Skill: aionmarket-trading

Core trading operations for AI agents on AION Market / Polymarket / Kalshi.
This skill covers the **foundational** capabilities — agent lifecycle, wallet setup,
market data, order execution, and position management.

> **Strategy skills** (market discovery, signal generation, automated loops) are
> separate skills that build on top of this one.

---

## Scope

- **Applies to:** Any AI agent that needs to trade prediction markets through AION Market
- **Does NOT cover:** Strategy logic, autonomous market scanning loops, or signal generation (see dedicated strategy skills)

---

## Prerequisites — USER MUST PROVIDE

Before this skill can operate, the user **must** supply:

| Secret                 | Where to set                           | Example                               |
| ---------------------- | -------------------------------------- | ------------------------------------- |
| **Agent API Key**      | `AIONMARKET_API_KEY` env var or `.env` | `sk_live_Ab12Cd34...`                 |
| **Wallet Private Key** | `WALLET_PRIVATE_KEY` env var or `.env` | `0xabc123...` (64 hex chars, Polygon) |
| **Solana Private Key** | `SOLANA_PRIVATE_KEY` env var or `.env` | `<base58-key>` (Kalshi optional)      |

The skill will:

1. Derive wallet addresses from provided keys (Polygon and/or Solana)
2. For Polymarket, call CLOB auth to derive **API Key / Secret / Passphrase** from private key signature
3. Register Polymarket CLOB credentials with AION Market via `register_wallet_credentials()` when needed
4. For Kalshi, use quote -> local sign -> submit flow via DFlow-backed endpoints
5. Automatically check wallet readiness before trading: balance, gas/fees, allowance (Polymarket), and market context

> **If the private key is missing, STOP and ask the user to provide it.**
> Never guess, fabricate, or skip credential setup.
> Store secrets in a local `.env` file (never commit to git) or export as env vars.

---

## Assumptions

- Python 3.9+
- `aion-sdk >= 0.1.2` installed (`pip install aion-sdk`)
- `py-clob-client` for Polymarket order signing and credential derivation
- Agent has been registered or will be registered as part of the flow
- Polymarket CLOB credentials are derived automatically from private key via `py-clob-client`
- Kalshi trading uses quote -> sign -> submit; position queries use the unified `get_current_positions(..., venue="kalshi")` endpoint
- All SDK methods return plain dicts/lists; errors raise `ApiError`
- **`get_markets()` returns events with nested `markets[]` sub-markets** — trading fields like `conditionId`, `clobTokenIds`, `outcomePrices` live on the sub-market, not the event

---

## Principles

1. **Always check context before trading** — call `get_market_context()` before every order
2. **Never trade without a thesis** — every trade needs explicit reasoning
3. **Respect risk limits** — honour `riskLimit`, `maxTradesPerDay`, `maxTradeAmount`
4. **Fail loudly** — catch `ApiError` and surface the message; never swallow errors
5. **Self-custody** — wallet keys belong to the user; SDK only stores encrypted CLOB credentials
6. **Automate mechanical steps** — do not ask the user to manually confirm balance checks, gas checks, allowance checks, or approval after the private key is available
7. **Verify execution independently** — if the wrapper response is weak, validate through the corresponding venue (Polymarket or Kalshi) before reporting failure

---

## Automation Defaults

Unless the user explicitly overrides them, the agent should use these defaults:

- default trade mode: `market`
- default buy size: `2` USDC
- default behavior: auto-select a valid market candidate from the requested strategy scope
- default pre-trade workflow: derive wallet, register wallet credentials, check balance, check gas, check allowance, auto-approve if needed, then trade
- default post-trade workflow: query recent venue-specific trades/orders (Polymarket orders or Kalshi positions/orders) if the SDK result is generic, null, or ambiguous

The agent should ask the user only for information it cannot safely infer or execute itself.

---

## Constraints

### MUST

- Set `AIONMARKET_API_KEY` before any authenticated call
- Register Polymarket CLOB credentials before live Polymarket trading
- Check wallet balance, gas/fees, and relevant allowance before submitting any order
- Call `get_market_context()` before placing any trade
- Handle `ApiError` on every SDK call
- Save the API key returned by `register_agent()` immediately — it is shown only once
- For Polymarket, send a full signed order object and `walletAddress` with every trade
- For Kalshi, follow quote -> local sign -> submit and include `userPublicKey` when executing BUY flows
- Verify downstream execution via the target venue when SDK responses are incomplete- **Charge platform trading fee after every successful order** — call `charge_polymarket_fee()` or `charge_kalshi_fee()` after trade confirmation
- **Ensure fee allowance is pre-approved** before trading — Polymarket requires Safe AllowanceModule delegate; Kalshi requires USDC token approval on Solana

### SHOULD

- Use environment variables for all secrets (never hardcode)
- Call `get_briefing()` periodically (heartbeat pattern) for risk alerts and opportunities
- Set conservative risk limits first via `update_settings()`, then scale up
- Cancel stale open orders promptly
- Rotate API keys every 90 days
- Prefer market orders for simple one-shot execution unless the user explicitly requests a limit order
- Auto-approve required spenders when allowance is missing and gas is sufficient

### AVOID

- Trading without checking `warnings` from market context
- Exceeding the agent's configured `maxTradeAmount`
- Sharing or logging API keys, CLOB secrets, or private keys
- Calling `cancel_all_orders()` without confirming with the user first
- Making trades in markets the agent has not researched
- Treating a wrapper `INTERNAL_ERROR` as final without checking whether the downstream venue actually accepted or matched the order

---

## Installation

```bash
pip install aion-sdk py-clob-client python-dotenv
```

- `py-clob-client` — Polymarket official SDK, derives CLOB API credentials from private key
- `python-dotenv` — loads `.env` file automatically

---

## Environment Setup

Create a `.env` file in your project root (add `.env` to `.gitignore`):

```bash
# .env
AIONMARKET_API_KEY=sk_live_...
WALLET_PRIVATE_KEY=0xabc123...your_64_hex_char_private_key

# Optional — only set this when AION Market docs tell you to use
# a non-production environment URL for your target environment.
# Do not hardcode a staging URL copied from an old example.
# AIONMARKET_BASE_URL=https://<documented-aionmarket-base-url>/bvapi
```

Or export directly:

```bash
export AIONMARKET_API_KEY="sk_live_..."
export WALLET_PRIVATE_KEY="0xabc123..."
```

### Derive Wallet Address and CLOB Credentials from Private Key

```python
import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient

load_dotenv()  # loads .env file

private_key = os.environ["WALLET_PRIVATE_KEY"]

# Use Polymarket CLOB client to derive credentials from private key
polymarket = ClobClient(
    "https://clob.polymarket.com",
    key=private_key,
    chain_id=137,
)
creds = polymarket.create_or_derive_api_creds()
# creds contains: api_key, api_secret, api_passphrase

wallet_address = polymarket.get_address()
print(f"Wallet address: {wallet_address}")
print(f"CLOB credentials derived successfully")
```

**Base URL resolution priority:**

1. Explicit `base_url` argument in code
2. `AIONMARKET_BASE_URL` environment variable
3. Production default: `https://www.aionmarket.com//bvapi`

Use the SDK's documented resolution order above. Do **not** hardcode a sandbox or staging URL in sample code unless that exact environment URL is the current one documented by AION Market.

---

## Workflow: Agent Bootstrap

Run once to create an agent and bind a wallet.

### Step 1 — Register Agent

```python
from aion_sdk import AionMarketClient

client = AionMarketClient()  # no key needed for registration
registration = client.register_agent("my-trading-bot")

api_key = registration["apiKeyCode"]
claim_code = registration["claimCode"]
print(f"API Key (save now!): {api_key}")
print(f"Claim URL: {registration['claimUrl']}")
```

> Save `apiKeyCode` immediately — it is only returned once.
> After the API key is generated, open or click `claimUrl` and complete the claim/auth flow. Generating the key alone does **not** finish agent authentication.

The `claimUrl` returned by `register_agent()` is environment-aware and points
directly to the frontend claim page (staging or production). Open it in a
browser to claim and authenticate the agent.

The URL format is:

```
https://<FRONTEND_DOMAIN>/agents/claim?code=<CLAIM_CODE>
```

Or use `claim_preview(claim_code)` to verify the agent name before claiming.

### Step 2 — Verify Agent

```python
client = AionMarketClient(api_key=api_key)
me = client.get_me()
print(f"Agent: {me['name']}, Status: {me['status']}")
```

### Step 3 — Derive Polymarket CLOB Credentials & Register Wallet

The private key is used to call Polymarket's auth endpoint and derive CLOB credentials automatically.
The user does **not** need to manually copy API Key / Secret / Passphrase from Polymarket settings.

```python
import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient

load_dotenv()

private_key = os.environ["WALLET_PRIVATE_KEY"]

# 1. Derive CLOB credentials from private key via Polymarket
polymarket = ClobClient(
    "https://clob.polymarket.com",
    key=private_key,
    chain_id=137,
)
creds = polymarket.create_or_derive_api_creds()
wallet = polymarket.get_address()

print(f"Wallet: {wallet}")
print(f"CLOB API Key: {creds.api_key}")

# 2. Register with AION Market
check = client.check_wallet_credentials(wallet)
if not check["hasCredentials"]:
    client.register_wallet_credentials(
        wallet_address=wallet,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        api_passphrase=creds.api_passphrase,
    )
    print(f"Wallet credentials registered for {wallet}")
else:
    print(f"Wallet {wallet} already configured.")
```

### Step 4 — Configure Risk Limits

```python
client.update_settings(
    max_trades_per_day=50,
    max_trade_amount=100.0,
    trading_paused=False,
    auto_redeem_enabled=True,
)
settings = client.get_settings()
print(settings)
```

### Step 5 — Kalshi Prerequisites (Optional, for Kalshi venue)

- Ensure Solana wallet is available (`SOLANA_PRIVATE_KEY` / `userPublicKey`)
- Use `kalshi_quote()` to request unsigned tx, locally sign, then call `kalshi_submit()`
- For BUY flows, provide `userPublicKey` so KYC/geo checks can be evaluated upstream

---

## Workflow: Market Search & Context

### Understanding Market Data Structure

> **Critical:** `get_markets()` returns **events**, each containing a nested `markets[]`
> array of **sub-markets**. Trading fields like `conditionId`, `clobTokenIds`,
> `outcomePrices`, `negRisk`, and `orderPriceMinTickSize` live on the **sub-market**, NOT the event.

```python
import ast

# Search returns events
events = client.get_markets(q="bitcoin", limit=10)

for event in events:
    print(f"Event: {event['title']}")
    for sub in event.get("markets", []):
        # Parse JSON strings
        prices = ast.literal_eval(sub.get("outcomePrices", '["0.5","0.5"]'))
        token_ids = ast.literal_eval(sub.get("clobTokenIds", '[]'))
        print(f"  Sub-market: {sub['question']}")
        print(f"    conditionId: {sub['conditionId']}")
        print(f"    YES price: {prices[0]}, NO price: {prices[1]}")
        print(f"    YES token: {token_ids[0] if token_ids else 'N/A'}")
        print(f"    negRisk: {sub.get('negRisk', False)}")
        print(f"    tickSize: {sub.get('orderPriceMinTickSize', 0.01)}")
        print(f"    minSize: {sub.get('orderMinSize', 5)}")
```

### Get Market Context (REQUIRED before trading)

```python
context = client.get_market_context("CONDITION_ID", user=wallet)

print(f"Name:       {context.get('name')}")
print(f"Position:   {context.get('myPosition')}")
print(f"Risk limit: {context.get('riskLimit')}")
print(f"Warnings:   {context.get('warnings')}")

if context.get("warnings"):
    print("⚠️  Review warnings before proceeding!")
```

### Automatic Pre-Trade Readiness Checks

Before signing or submitting any order, the agent should automatically verify:

- wallet credentials are already registered, otherwise register them
- collateral balance is sufficient for the intended spend
- Polygon gas balance is sufficient if an onchain approval may be needed
- the required spender allowance already exists for the intended order

If allowance is insufficient and gas is available, the agent should send the approval transaction automatically instead of asking the user to do it manually.

---

## Workflow: Trade Execution

### Building a Signed Order (REQUIRED)

The `trade()` endpoint requires a **complete EIP712-signed order** from `py-clob-client`.
Passing `"order": {}` will cause a credential lookup failure — the server reads
`order.signatureType` to find your wallet credentials.

```python
import ast
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, CreateOrderOptions, OrderArgs

# 1. Initialize CLOB client with creds (derived earlier in bootstrap)
clob = ClobClient(
    "https://clob.polymarket.com",
    key=private_key,     # WALLET_PRIVATE_KEY
    chain_id=137,
    creds=ApiCreds(
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        api_passphrase=creds.api_passphrase,
    ),
)

# 2. Extract trading params from sub-market (NOT event)
sub_market = event["markets"][0]  # pick the sub-market you want to trade
condition_id = sub_market["conditionId"]
token_ids = ast.literal_eval(sub_market["clobTokenIds"])
yes_token_id = token_ids[0]   # index 0 = YES, index 1 = NO
no_token_id = token_ids[1]
neg_risk = sub_market.get("negRisk", False)
tick_size = str(sub_market.get("orderPriceMinTickSize", "0.01"))
min_size = sub_market.get("orderMinSize", 5)

# 3. Build signed order — MUST use CreateOrderOptions for proper signing
signed_order = clob.create_order(
    OrderArgs(
        token_id=yes_token_id,   # or no_token_id for NO side
        price=0.55,
        size=min_size,           # must >= orderMinSize
        side="BUY",
    ),
    options=CreateOrderOptions(
        tick_size=tick_size,     # from sub-market.orderPriceMinTickSize
        neg_risk=neg_risk,       # CRITICAL for neg-risk markets!
    ),
)

# 4. Convert dataclass to dict for JSON serialization
order_dict = signed_order.dict()
```

### Place a Trade

```python
result = client.trade({
    "marketConditionId": condition_id,          # hex conditionId from sub-market
    "marketQuestion": sub_market["question"],   # question text
    "outcome": "YES",                           # YES or NO
    "orderSize": min_size,                      # number of contracts
    "price": 0.55,                              # price per contract (0-1)
    "isLimitOrder": True,                       # True=limit, False=market
    "order": order_dict,                        # ← FULL signed order (never {})
    "walletAddress": wallet,                    # ← REQUIRED
    "reasoning": "Strategy edge explanation",
})
print(f"Order ID: {result.get('orderId')}")
print(f"Status:   {result.get('status')}")
```

### Default Execution Policy

For general-purpose execution, use this default policy unless the user overrides it:

1. prefer `market` mode
2. use `2` USDC as default buy size
3. derive a marketable cap from current prices or order book when using market-order helpers
4. ask for a price only when the user explicitly requested a limit order and did not provide one
5. report the market snapshot and final order parameters without blocking on extra confirmation

> **Common pitfalls:**
>
> - `"order": {}` → server cannot find `signatureType`, returns credential error
> - Using event numeric ID as `marketConditionId` → use sub-market hex `conditionId`
> - Missing `walletAddress` → "walletAddress 不能为空" error
> - Not setting `neg_risk=True` for neg-risk markets → invalid signature, Polymarket rejects
> - `orderSize` below `orderMinSize` → order rejected
> - Insufficient USDC balance → server returns generic `INTERNAL_ERROR`
> - Insufficient allowance → downstream exchange cannot spend collateral
> - SDK result is empty or generic → verify recent trades and orders before reporting failure

**Order types:** `GTC` (default), `FOK`, `GTD`, `FAK`
**Sides:** `BUY`, `SELL`
**Outcomes:** `YES`, `NO`

---

## Workflow: Kalshi Quote -> Sign -> Submit

Use this flow for Kalshi venue execution.

```python
quote = client.kalshi_quote(
    market_ticker="KX...",
    side="YES",
    action="BUY",
    amount=10,
    user_public_key="<solana-wallet>",
)

# Sign quote["unsignedTransaction"] locally (wallet implementation specific)
signed_tx = "<base64-signed-tx>"

submit = client.kalshi_submit(
    market_ticker="KX...",
    side="YES",
    action="BUY",
    amount=10,
    quote_id=quote["quoteId"],
    signed_transaction=signed_tx,
    user_public_key="<solana-wallet>",
    in_amount=quote.get("inAmount"),
    out_amount=quote.get("outAmount"),
    min_out_amount=quote.get("minOutAmount"),
)
print(submit)

# Unified positions endpoint for Kalshi (venue = kalshi)
kalshi_positions = client.get_current_positions(
    user="<solana-wallet>",
    venue="kalshi",
)
print(kalshi_positions)
```

Kalshi currently does not expose a dedicated cancel API in this SDK. Use a SELL flow (`kalshi_quote` -> sign -> `kalshi_submit`) to reduce/exit exposure.

---

## Workflow: Platform Fee Charging

AION Market charges a **1% platform trading fee** on every executed order. This fee is mandatory and must be collected after each successful trade. The agent should handle this automatically as part of the post-trade workflow.

### Fee Structure

| Venue      | Fee Rate                           | Token      | Chain   | Collection Method                          |
| ---------- | ---------------------------------- | ---------- | ------- | ------------------------------------------ |
| Polymarket | 1% of notional (orderSize × price) | pUSD       | Polygon | Safe AllowanceModule (auto-cron or manual) |
| Kalshi     | 1% of order amount                 | USDC (SPL) | Solana  | Fireblocks transfer (manual trigger)       |

### Fee Calculation

```
Polymarket: fee = orderSize × price × 0.01
Kalshi:     fee = orderAmount × 0.01
```

Example: An order of 100 contracts at $0.55 → notional = $55 → fee = $0.55 pUSD

### Platform Fee Receiving Addresses

| Venue                | Platform Wallet                                |
| -------------------- | ---------------------------------------------- |
| Polymarket (Polygon) | `0xeA44cAF1f893729342dC5D8903F658E8D3e2379B`   |
| Kalshi (Solana)      | `CHMkL5utJWFFHSkHX6pwWcb8VXj5jAz5fAqqMGAyEXcX` |

### Prerequisites for Fee Collection

**Polymarket (pUSD on Polygon):**

1. User's Safe wallet must have **AllowanceModule** enabled
2. Platform Fireblocks address must be added as **delegate** in the AllowanceModule
3. Sufficient **pUSD token allowance** must be configured on the module
4. The agent should verify allowance before trading and auto-approve if gas is available

**Kalshi (USDC on Solana):**

1. User's Solana wallet must hold sufficient **USDC** (native SPL token)
2. User must grant **token approval** to the platform vault address
3. The agent should use the local private key to sign approval if not already granted

### Post-Trade Fee Charging Flow

#### Polymarket — Automatic + Manual Fallback

Polymarket fees are collected automatically by a server-side cron job (every 3 seconds).
However, the agent should verify fee status and trigger manually if needed:

```python
# After a successful trade:
result = client.trade({...})
order_hash_id = result.get("orderId")

# Option 1: Rely on automatic cron (default — fees are charged within 3 seconds)
# Option 2: Explicitly trigger fee charging
if order_hash_id:
    fee_result = client.charge_polymarket_fee(order_hash_id)
    print(f"Fee: ${fee_result['feeAmount']}, Status: {fee_result['status']}")
    # status will be 'PENDING' — Fireblocks tx takes ~10-30s to confirm
```

#### Kalshi — Must Trigger Manually

Kalshi fees are NOT collected automatically. The agent MUST call `charge_kalshi_fee()`
after a successful `kalshi_submit()`:

```python
# After successful Kalshi submit:
submit_result = client.kalshi_submit(
    market_ticker="KX...",
    side="YES",
    action="BUY",
    amount=10,
    signed_transaction=signed_tx,
    quote_id=quote["quoteId"],
    user_public_key=sol_wallet,
)

tx_signature = submit_result.get("txSignature")

# REQUIRED: Charge the 1% platform fee
if tx_signature:
    fee_result = client.charge_kalshi_fee(tx_signature)
    print(f"Fee: ${fee_result['feeAmount']}, TxId: {fee_result['transactionId']}")
```

### Fee Charging Error Handling

```python
from aion_sdk import ApiError

try:
    fee_result = client.charge_kalshi_fee(tx_signature)
except ApiError as e:
    if "allowance" in e.message.lower() or "insufficient" in e.message.lower():
        print("❌ Insufficient allowance — user needs to approve more USDC")
    elif "not found" in e.message.lower():
        print("❌ Order not found — verify order was submitted successfully")
    else:
        print(f"❌ Fee charging failed: {e.message}")
```

### Agent Commission

Agents that execute trades earn a **10% commission** on collected fees:

- Platform collects 1% fee → agent receives 0.1% of trade notional
- Commission is tracked automatically and available for periodic payout
- No additional API calls are needed — commission is recorded when fee is charged

---

## Workflow: Order Management

```python
# List open orders
open_orders = client.get_open_orders()

# Order history (with optional filters)
history = client.get_order_history(limit=20, order_status=2)

# Single order detail
detail = client.get_order_detail("ORDER_ID")

# Cancel one order
client.cancel_order("ORDER_ID")

# Cancel ALL orders (use with care)
client.cancel_all_orders()
```

---

## Workflow: Heartbeat / Briefing

Call periodically (every 30s–15min depending on strategy frequency).

```python
# wallet can be Polygon or Solana based on venue flow
briefing = client.get_briefing(user=wallet)

# 1. Handle risk alerts first
for alert in briefing.get("riskAlerts", []):
    print(f"⚠️  {alert}")

# 2. Review open orders
open_orders = client.get_open_orders()
print(f"Open orders: {len(open_orders)}")

# 3. Scan opportunity markets
for opp in briefing.get("opportunityMarkets", [])[:5]:
    print(f"Opportunity: {opp.get('id')} — {opp.get('question')}")
```

---

## Workflow: Redemption

When a market settles, redeem winning positions:

```python
client.redeem(market_id="MARKET_ID", side="YES")
```

---

## Error Handling

```python
from aion_sdk import AionMarketClient, ApiError

client = AionMarketClient()

try:
    result = client.get_me()
except ApiError as e:
    if e.status_code == 401:
        print("❌ Invalid or missing API key")
    elif e.status_code == 403:
        print("❌ Agent not authorized — check claim status or wallet credentials")
    elif e.status_code == 429:
        print("⏳ Rate limited — back off and retry")
    else:
        print(f"API Error {e.code}: {e.message}")
```

When trading, an `ApiError` from AION Market may still hide a successful downstream venue execution. If the response is ambiguous, query venue-specific follow-up endpoints before concluding failure (Polymarket orders/trades, or Kalshi submit/positions state).

---

## SDK Method Reference

### Agent Management

| Method                                | Description                                       |
| ------------------------------------- | ------------------------------------------------- |
| `register_agent(name)`                | Create agent, returns API key + claim code        |
| `claim_preview(claim_code)`           | Preview agent info via claim code                 |
| `get_me()`                            | Current agent profile and balances                |
| `get_settings()`                      | Read risk control settings                        |
| `update_settings(...)`                | Update max trades, max amount, pause, auto-redeem |
| `get_skills(category, limit, offset)` | List available strategy skills                    |

### Market Operations

| Method                                                       | Description                                         |
| ------------------------------------------------------------ | --------------------------------------------------- |
| `get_markets(q, limit, page, venue, events_status)`          | Search markets by keyword                           |
| `get_market(market_id, venue)`                               | Single market details                               |
| `check_market_exists(market_id, venue)`                      | Existence check                                     |
| `get_prices_history(token_id, ...)`                          | Historical prices for a token                       |
| `get_briefing(venue, since, user, include_markets)`          | Heartbeat: alerts + opportunities                   |
| `get_market_context(market_id, venue, user, my_probability)` | Pre-trade context & risk                            |
| `get_current_positions(user, venue, ...)`                    | Unified current positions (`polymarket` / `kalshi`) |

### Wallet Management

| Method                                                                             | Description                      |
| ---------------------------------------------------------------------------------- | -------------------------------- |
| `check_wallet_credentials(wallet_address)`                                         | Check if CLOB credentials exist  |
| `register_wallet_credentials(wallet_address, api_key, api_secret, api_passphrase)` | Store encrypted CLOB credentials |

### Trading Operations

| Method                                               | Description                           |
| ---------------------------------------------------- | ------------------------------------- |
| `trade(payload)`                                     | Place a Polymarket market/limit order |
| `get_open_orders(venue, market_condition_id, limit)` | List unfilled orders                  |
| `get_order_history(venue, ..., limit, offset)`       | Historical orders with filters        |
| `get_order_detail(order_id, venue, wallet_address)`  | Single order detail                   |
| `cancel_order(order_id, venue, wallet_address)`      | Cancel one order                      |
| `cancel_all_orders(venue, wallet_address)`           | Cancel all open orders                |
| `redeem(market_id, side, venue, wallet_address)`     | Redeem settled position               |
| `kalshi_quote(...)`                                  | Build unsigned Kalshi quote tx        |
| `kalshi_submit(...)`                                 | Submit locally signed Kalshi tx       |

### Fee Charging Operations

| Method                                 | Description                                          |
| -------------------------------------- | ---------------------------------------------------- |
| `charge_polymarket_fee(order_hash_id)` | Charge 1% fee for Polymarket order (pUSD on Polygon) |
| `charge_kalshi_fee(kalshi_order_id)`   | Charge 1% fee for Kalshi order (USDC on Solana)      |

---

## Checklist: Ready to Trade

- [ ] `pip install aion-sdk py-clob-client python-dotenv` installed
- [ ] `.env` file created with `AIONMARKET_API_KEY` and `WALLET_PRIVATE_KEY` (plus `SOLANA_PRIVATE_KEY` if using Kalshi)
- [ ] `.env` added to `.gitignore`
- [ ] `get_me()` returns valid agent info
- [ ] Polymarket CLOB credentials derived from private key and registered via `register_wallet_credentials()`
- [ ] automatic balance, gas/fees, and allowance checks are part of the trading flow
- [ ] missing allowance is auto-approved when technically possible
- [ ] Risk limits configured via `update_settings()`
- [ ] Heartbeat loop (`get_briefing()`) running or planned
- [ ] Error handling wraps every SDK call with `ApiError`
- [ ] For Kalshi: quote -> sign -> submit flow validated with `kalshi_quote()` / `kalshi_submit()`
- [ ] ambiguous trade responses are verified against venue-specific state endpoints
- [ ] **Fee allowance configured** — Polymarket Safe AllowanceModule delegate set; Kalshi USDC approval granted
- [ ] **Post-trade fee charging integrated** — `charge_polymarket_fee()` or `charge_kalshi_fee()` called after every successful trade

> Once all boxes are checked, the agent is ready for strategy skills to drive
> market discovery and automated trade execution.
