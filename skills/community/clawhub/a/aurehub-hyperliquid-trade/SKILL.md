---
name: hyperliquid-trade
description: "Trade on Hyperliquid — spot and perpetual futures. Supports market orders (IOC), limit orders (GTC), leverage setting, WDK wallet, and USDC deposit from Arbitrum. Triggers: buy ETH spot, sell BTC, long ETH, short BTC, open long, open short, close position, perp trade, check balance, Hyperliquid positions, limit order, limit buy, limit sell, open orders, cancel order, modify order, GTC, deposit USDC, fund wallet, bridge USDC."
license: MIT
compatibility: "Requires Node.js >= 20.19.0"
metadata:
  author: aurehub
  version: "1.3.0"
---

# hyperliquid-trade

Trade spot and perpetual futures on Hyperliquid L1 using IOC market orders.

## When to Use

- **Spot**: buy or sell any token listed on Hyperliquid spot markets
- **Perps**: open long/short or close perpetual futures positions
- **Balance**: check spot token balances or perp positions and margin
- **Deposit**: bridge USDC from Arbitrum One to Hyperliquid L1

## External Communications

This skill connects to the Hyperliquid API (`api_url` in `hyperliquid.yaml`, default `https://api.hyperliquid.xyz`). Inform the user before the first external call in each session. On first setup, installs dependencies via `npm install`.

## Environment & Security Declaration

### Required config files

| File | Purpose |
|------|---------|
| `~/.aurehub/.wdk_vault` | WDK encrypted vault (created by xaut-trade setup) |
| `~/.aurehub/.wdk_password` | Vault password (mode 0600, created by xaut-trade setup) |
| `~/.aurehub/hyperliquid.yaml` | Network, API URL, risk thresholds |

### Optional environment variables (in `~/.aurehub/.env`)

| Variable | Purpose | Default |
|----------|---------|---------|
| `WDK_ACCOUNT_INDEX` | HD derivation index (0-based) for wallet address | `0` |
| `ARBITRUM_RPC_URL` | Arbitrum One JSON-RPC endpoint — required for `deposit.js` | *(none; public: `https://arb1.arbitrum.io/rpc`)* |

### Security safeguards

- Private key is decrypted from vault in memory only, never stored
- Decrypted key material zeroed from memory after use
- All external API responses treated as untrusted numeric data
- Every trade requires explicit user confirmation per thresholds in `hyperliquid.yaml`

## Environment Readiness Check (run first on every session)

`<skill-dir>` = directory containing this SKILL.md.
`<scripts-dir>` = `<skill-dir>/scripts`.

Run these checks before handling any intent (except knowledge queries):

| Step | Check | Type | Action |
|------|-------|------|--------|
| 1 | `~/.aurehub/.wdk_vault` exists | HARD STOP | Load [references/onboarding.md](references/onboarding.md) and guide the user through setup. |
| 2 | `~/.aurehub/.wdk_password` exists | HARD STOP | Load [references/onboarding.md](references/onboarding.md) and guide the user through setup. |
| 3 | `~/.aurehub/hyperliquid.yaml` exists | AUTO-FIX | `cp <skill-dir>/config.example.yaml ~/.aurehub/hyperliquid.yaml` |
| 4 | `node -e "const [maj,min]=process.version.slice(1).split('.').map(Number);if(maj<20||(maj===20&&min<19))process.exit(1)"` passes | HARD STOP | "Node.js >= 20.19.0 is required. Please upgrade." |
| 5 | `<scripts-dir>/node_modules` exists | AUTO-FIX | `cd <scripts-dir> && npm install` |
| 6 | `node <scripts-dir>/balance.js address` succeeds | HARD STOP | Report error JSON; load [references/onboarding.md](references/onboarding.md) |

If all pass: source `~/.aurehub/.env`, run **Account Selection** (below), then **Wallet-Ready Registration**, then proceed to intent detection.

## Account Selection

If the user specifies a wallet index (e.g. "use wallet 2", "account 1", "wallet 3"), remember that index for the entire session. Append `--account N` to **every** `node balance.js`, `node trade.js`, and `node limit-order.js` command in this session.

If the user does not specify an account, do not append `--account` — the default from `WDK_ACCOUNT_INDEX` in `.env` (or `0`) is used automatically.

## Wallet-Ready Registration

Run immediately after environment checks pass. Derive WALLET_ADDRESS from check 6's output (if an account was selected above, include `--account N`):

```bash
source ~/.aurehub/.env
WALLET_ADDRESS=$(node <scripts-dir>/balance.js address | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).address")
```

If this fails, skip registration silently and continue.

1. `REGISTERED=$(cat ~/.aurehub/.registered 2>/dev/null)`
2. If `"$REGISTERED"` starts with `"$WALLET_ADDRESS:"` → already registered, silent skip; return immediately
3. If `RANKINGS_OPT_IN` != `"true"`:
   - Check marker: `PROMPTED=$(cat ~/.aurehub/.rankings_prompted 2>/dev/null)`
   - If marker starts with `"$WALLET_ADDRESS:"` → skip; return immediately
   - Otherwise ask once: "Join XAUT activity rankings now? (yes/no)"
     - If user says `no`: `echo "$WALLET_ADDRESS:declined" > ~/.aurehub/.rankings_prompted`; return
     - If user says `yes`:
       - If `NICKNAME` is empty: ask user for nickname
       - Persist opt-in in `~/.aurehub/.env` (`RANKINGS_OPT_IN=true`, `NICKNAME=<value>`)
       - Re-source env: `source ~/.aurehub/.env`
       - Continue to step 4
4. If `RANKINGS_OPT_IN` == `"true"`:
   - If `NICKNAME` is empty: ask "You're opted in to XAUT activity rankings — what nickname would you like to appear as?", then persist to `~/.aurehub/.env` and re-source
   - Register:
   ```bash
   NICKNAME_ESC=$(printf '%s' "$NICKNAME" | sed 's/\\/\\\\/g; s/"/\\"/g')
   REGISTER_RESP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
     https://xaue.com/api/rankings/participants \
     -H 'Content-Type: application/json' \
     -d "{\"wallet_address\":\"$WALLET_ADDRESS\",\"nickname\":\"$NICKNAME_ESC\",\"source\":\"agent\"}")
   ```
   - HTTP 200 or 201: `echo "$WALLET_ADDRESS:$NICKNAME" > ~/.aurehub/.registered`; inform: "Registered with nickname: $NICKNAME"
   - Any other status: silent continue, do not write marker file

Only prompt once per wallet. The `.rankings_prompted` and `.registered` markers ensure idempotency across sessions.

## Intent Detection

| User says | Action |
|-----------|--------|
| buy ETH / purchase BTC / spot buy | `trade.js spot buy` |
| sell SOL / spot sell ETH | `trade.js spot sell` |
| long ETH / open long BTC 10x / go long | `trade.js perp open ... long` |
| short BTC / open short ETH / go short | `trade.js perp open ... short` |
| close position / close ETH / flat / exit | `trade.js perp close` (auto-detects direction) |
| balance / holdings / positions / how much / 查看余额 / 查看持仓 / 持仓 | **Always run both**: `balance.js spot` + `balance.js perp`. Never return only one. |
| setup / onboarding / first time | Load [references/onboarding.md](references/onboarding.md) |
| Insufficient info (no coin or amount) | Ask for the missing details before proceeding |
| limit buy ETH at 3000 / limit order / limit sell | Load [references/limit-order.md](references/limit-order.md); run `limit-order.js place` |
| open orders / my orders / list orders | Load [references/limit-order.md](references/limit-order.md); run `limit-order.js list` |
| cancel order / cancel limit | Load [references/limit-order.md](references/limit-order.md); run `limit-order.js cancel` |
| change order price / update order / modify order | Load [references/limit-order.md](references/limit-order.md); run `limit-order.js modify` |
| deposit USDC / fund wallet / bridge USDC / 充值 / 存款 / 往 HL 存钱 | Run `deposit.js` flow (see **Deposit Flow** below) |
| withdraw USDC / withdraw to Arbitrum / 提现 / 取款 / 把钱取出来 | Run `withdraw.js` flow (see **Withdraw Flow** below) |

## Resolving HL_SCRIPTS_DIR

Use `<skill-dir>/scripts` as the scripts directory. To find `<skill-dir>` at runtime:

```bash
# 1. Git repo fallback
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -n "$GIT_ROOT" ] && [ -d "$GIT_ROOT/skills/hyperliquid-trade/scripts" ] && HL_SCRIPTS_DIR="$GIT_ROOT/skills/hyperliquid-trade/scripts"
# 2. Bounded home search
[ -z "$HL_SCRIPTS_DIR" ] && HL_SCRIPTS_DIR=$(dirname "$(find -L "$HOME" -maxdepth 6 -type f -path "*/hyperliquid-trade/scripts/balance.js" 2>/dev/null | head -1)")
echo "$HL_SCRIPTS_DIR"
```

## Balance Flow

Load [references/balance.md](references/balance.md) for the full flow.

```bash
node "$HL_SCRIPTS_DIR/balance.js" spot
node "$HL_SCRIPTS_DIR/balance.js" perp
```

Parse the JSON output and present balances in a human-readable table.

## Spot Trade Flow

Load [references/spot-trade.md](references/spot-trade.md) for the full flow.

1. Confirm intent: coin, direction (buy/sell), size
2. Run balance check to verify sufficient USDC/token
3. Run: `node "$HL_SCRIPTS_DIR/trade.js" spot <buy|sell> <COIN> <SIZE>`
4. Read preview JSON; apply confirmation logic per `requiresConfirm`/`requiresDoubleConfirm` flags (same as limit orders)
5. After user confirms, re-run: `node "$HL_SCRIPTS_DIR/trade.js" spot <buy|sell> <COIN> <SIZE> --confirmed`
6. Use the last JSON line as the result; report fill price and outcome
7. **After a spot buy**: `filledSz` in the result reflects the ordered quantity, not the net-of-fees received amount (Hyperliquid deducts taker fees ~0.035% from the received tokens). If the user immediately wants to sell, run `balance.js spot` first to get the actual available balance and use that as the sell size.

## Perp Trade Flow

Load [references/perp-trade.md](references/perp-trade.md) for the full flow.

**Open position:**
1. Confirm intent: coin, direction (long/short), size, leverage, margin mode
2. Run: `node "$HL_SCRIPTS_DIR/trade.js" perp open <COIN> <long|short> <SIZE> [--leverage <N>] [--cross|--isolated]`
3. Read preview JSON; apply confirmation logic per `requiresConfirm`/`requiresDoubleConfirm` flags
4. After user confirms, re-run with `--confirmed`; use the last JSON line as the result

**Close position:**
1. Show current position from `balance.js perp`; confirm size to close
2. Run: `node "$HL_SCRIPTS_DIR/trade.js" perp close <COIN> <SIZE>`
3. Read preview JSON; apply confirmation logic
4. After user confirms, re-run with `--confirmed`; use the last JSON line as the result

## Confirmation Thresholds

Thresholds are read from `~/.aurehub/hyperliquid.yaml`. Defaults: `confirm_trade_usd=100`, `large_trade_usd=1000`, `leverage_warn=20`.

For **spot**: threshold applies to trade value (size × est. price).
For **perps**: threshold applies to margin deposited (size × est. price ÷ leverage).

```
< confirm_trade_usd    →  show preview, execute without prompting
≥ confirm_trade_usd    →  show preview, single confirmation
≥ large_trade_usd      →  show preview, double confirmation required
leverage ≥ leverage_warn  →  extra warning line before confirmation
```

Trade preview format (present to user before prompting):
```
Action:      <Open Long ETH (Perpetual) | Buy ETH (Spot)>
Size:        <0.1 ETH>
Leverage:    <10x Cross>           ← perp only
Est. price:  ~$<3,200>  (IOC, <slippage_pct>% slippage budget — default 5%, configurable in hyperliquid.yaml)
Margin used: ~$<320> USDC         ← perp only
Trade value: ~$<320> USDC         ← spot only
Confirm? [y/N]
```

`trade.js` outputs this as a `preview` JSON object. Parse the JSON and render the above format before prompting. Apply `requiresConfirm`/`requiresDoubleConfirm` flags for confirmation logic; if `leverageWarning: true`, add an extra warning line about high leverage; if `leverageChangeWarning: true`, add a warning: "Note: this leverage setting takes effect immediately and will apply to all existing cross-margin positions for this coin."

## Hard Stops

| Condition | Message |
|-----------|---------|
| Insufficient balance | "Insufficient balance: have $X, need $Y. Deposit at app.hyperliquid.xyz to top up." |
| Asset not found | "Asset X not found on Hyperliquid. Check the symbol and try again." |
| Leverage exceeds asset max | "Max leverage for ETH is Nx. Requested: Mx." |
| No open position (close) | "No open position found for ETH." |
| IOC order not filled | Relay the script's error verbatim — it includes the configured slippage % (e.g. "Order not filled — price moved beyond the 5% IOC limit. Check current price and retry.") |
| Node.js < 20.19 | "Node.js >= 20.19.0 required. Please upgrade: https://nodejs.org" |
| API unreachable | "Hyperliquid API unreachable. Check network or `api_url` in `~/.aurehub/hyperliquid.yaml`." |

## Deposit Flow

Bridges USDC from Arbitrum One to Hyperliquid L1 using the HL bridge contract.
The same wallet address receives USDC on HL within ~1 minute.

**Prerequisites:**
- `ARBITRUM_RPC_URL` must be set in `~/.aurehub/.env` (e.g. `https://arb1.arbitrum.io/rpc`)
- Wallet must have USDC on Arbitrum One (native USDC, not USDC.e)
- Wallet must have a small amount of ETH on Arbitrum One for gas

**Steps:**

1. Confirm intent: amount in USDC (minimum 5 USDC — amounts below minimum are permanently lost)
2. Check `ARBITRUM_RPC_URL` is set; if missing, instruct user to add it to `~/.aurehub/.env` and stop
3. Run preview: `node "$HL_SCRIPTS_DIR/deposit.js" <amount>`
4. Parse preview JSON; apply confirmation logic per `requiresConfirm`/`requiresDoubleConfirm` flags
5. After user confirms, re-run with `--confirmed`
6. Report the `txHash` and credit note from the result

**Preview format (render before prompting):**
```
Action:       Deposit USDC → Hyperliquid L1
Amount:       <100> USDC
From/To:      <0x...> (same address on HL)
USDC balance: <150.00> USDC (Arbitrum)
ETH balance:  <0.005> ETH (Arbitrum, for gas)
Credit time:  ~1 minute
Confirm? [y/N]
```

**Hard stops:**

| Condition | Message |
|-----------|---------|
| `ARBITRUM_RPC_URL` not set | "Add ARBITRUM_RPC_URL to ~/.aurehub/.env first. Public RPC: https://arb1.arbitrum.io/rpc" |
| Amount < 5 USDC | "Minimum deposit is 5 USDC. Smaller amounts are permanently lost by the bridge." |
| Insufficient USDC | "Insufficient USDC on Arbitrum. Have $X, need $Y." |
| No ETH for gas | "No ETH on Arbitrum One for gas. Bridge a small amount of ETH to Arbitrum first." |
| Wrong network | "ARBITRUM_RPC_URL points to wrong network. Must be Arbitrum One (chainId 42161)." |

## Withdraw Flow

Withdraws USDC from Hyperliquid L1 to Arbitrum One. Funds arrive at the same wallet address within ~5 minutes. A **1 USDC fee** is deducted by the bridge; no ETH is required.

**Steps:**

1. Confirm intent: amount in USDC (minimum 2 USDC — 1 USDC fee is deducted, so at least 1 USDC arrives)
2. Run preview: `node "$HL_SCRIPTS_DIR/withdraw.js" <amount>`
3. Parse preview JSON; apply confirmation logic per `requiresConfirm`/`requiresDoubleConfirm` flags
4. After user confirms, re-run with `--confirmed`
5. Report the net received amount and credit note

**Preview format (render before prompting):**
```
Action:       Withdraw USDC → Arbitrum One
Amount:       <10> USDC
Fee:          1 USDC (bridge fee)
Net received: <9> USDC
USDC balance: <13.63> USDC (Hyperliquid L1)
Withdrawable: <13.63> USDC
Credit time:  ~5 minutes
Confirm? [y/N]
```

**Hard stops:**

| Condition | Message |
|-----------|---------|
| Amount < 2 USDC | "Minimum withdrawal is 2 USDC (1 USDC fee is deducted)." |
| Insufficient withdrawable | "Insufficient withdrawable balance. Have $X, need $Y." |
| Margin locked | Append: "X USDC is locked as perp margin. Close positions to free up more." |

## Limit Order Flow

Load [references/limit-order.md](references/limit-order.md) for the full flow.

**Place a limit order:**
1. Confirm intent: coin, direction, price, size (ask for any missing details)
2. Run: `node "$HL_SCRIPTS_DIR/limit-order.js" place <spot|perp> <buy|sell|long|short> <COIN> <PRICE> <SIZE> [--leverage N] [--cross|--isolated]`
3. Read the `preview` JSON; apply confirmation logic per `references/limit-order.md`
4. After user confirms, re-run with `--confirmed` flag
5. Report fill outcome and order ID

**List / cancel / modify:**
1. Run the appropriate `limit-order.js` subcommand
2. For modify: always show a preview and ask for user confirmation before executing
3. When re-running modify with `--confirmed`, the script emits the preview JSON line first, then the result — use the **last** JSON line as the result
4. After a successful modify, the order ID changes (`oid` in the result is the new ID); update any stored order ID accordingly
5. Parse JSON and present result in a human-readable format
