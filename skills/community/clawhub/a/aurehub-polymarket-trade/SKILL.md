---
name: polymarket-trade
description: >
  Trade on Polymarket prediction markets on Polygon. Supports browsing markets,
  checking wallet/CLOB balance, and buying or selling YES/NO shares with safety gates.
  Wallet: WDK vault (~/.aurehub/.wdk_vault). Config: ~/.aurehub/polymarket.yaml.
  Triggers: buy YES, buy NO, sell shares, browse markets, check Polymarket balance,
  Polymarket trade, prediction market, what are the odds, redeem winnings, claim resolved positions.
license: MIT
compatibility: "Requires Node.js >= 18, Polygon RPC (HTTPS), and Polymarket CLOB API credentials."
metadata:
  author: aurehub
  version: "1.1.0"
---

# polymarket-trade

Trade on Polymarket prediction markets. Non-custodial — private key stays in your WDK vault.

## Prerequisites

Before any action, check prerequisites for the current flow and auto-fix what you can.

**Browse flow** (no wallet, no RPC, no CLOB needed): check step 4 only.
**Redeem flow** (no CLOB needed): check steps 1–5 in order.
**Balance / Trade / Setup flow**: check all steps 1–6 in order.

Step types:
- **HARD STOP** — cannot proceed; inform user and stop (these require prior xaut-trade setup).
- **AUTO-FIX** — run the command automatically, then continue.
- **INTERACTIVE** — run the script; it will print the wallet address and save credentials; report the result to the user.

| Step | Missing item | Type | Agent action |
|------|---|---|---|
| 1 | `~/.aurehub/.wdk_vault` | HARD STOP | Inform: xaut-trade must be installed and its wallet setup completed first. Stop. |
| 2 | `~/.aurehub/.wdk_password` | HARD STOP | Inform: xaut-trade must be installed and its wallet setup completed first. Stop. |
| 3 | `~/.aurehub/.env` missing | AUTO-FIX | Run: `cp <skill-dir>/.env.example ~/.aurehub/.env` |
| 3 | `~/.aurehub/.env` exists, `POLYGON_RPC_URL` absent | AUTO-FIX | Append `POLYGON_RPC_URL=https://polygon.drpc.org` to `~/.aurehub/.env` |
| 4 | `~/.aurehub/polymarket.yaml` missing | AUTO-FIX | Run: `cp <skill-dir>/config.example.yaml ~/.aurehub/polymarket.yaml` |
| 5 | `node_modules` missing in `<skill-dir>/scripts/` | AUTO-FIX | Run: `npm install` in `<skill-dir>/scripts/` |
| 6 | `~/.aurehub/.polymarket_clob` missing | INTERACTIVE | Run: `node <skill-dir>/scripts/setup.js` (only after steps 3–5 pass) |

On any auto-fix failure: stop and report the error with the manual remediation command.
After all fixes succeed, re-run the relevant checks and proceed.

### Optional environment variables (in `~/.aurehub/.env`)

| Variable | Purpose | Default |
|----------|---------|---------|
| `WDK_ACCOUNT_INDEX` | HD derivation index (0-based) for wallet address | `0` |

After prerequisites pass: if the user's message matches browse flow (contains "browse", "what markets", "what are the odds"), skip registration and proceed directly to intent detection. Otherwise run **Account Selection**, then **Wallet-Ready Registration** (below) before proceeding to intent detection.

## Account Selection

If the user specifies a wallet index (e.g. "use wallet 2", "account 1", "wallet 3"), remember that index for the entire session. Append `--account N` to **every** `node trade.js`, `node balance.js`, `node setup.js`, and `node redeem.js` command in this session.

If the user does not specify an account, do not append `--account` — the default from `WDK_ACCOUNT_INDEX` in `.env` (or `0`) is used automatically.

`<skill-dir>` is the directory containing this SKILL.md file.

## Resolving POLY_SCRIPTS_DIR

Use `<skill-dir>/scripts` as the scripts directory. To find it at runtime:

```bash
# 1. Git repo fallback
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -n "$GIT_ROOT" ] && [ -d "$GIT_ROOT/skills/polymarket-trade/scripts" ] && POLY_SCRIPTS_DIR="$GIT_ROOT/skills/polymarket-trade/scripts"
# 2. Bounded home search
[ -z "$POLY_SCRIPTS_DIR" ] && POLY_SCRIPTS_DIR=$(dirname "$(find -L "$HOME" -maxdepth 6 -type f -path "*/polymarket-trade/scripts/browse.js" 2>/dev/null | head -1)")
```

## Wallet-Ready Registration

Run after prerequisites pass for any wallet-requiring flow (not browse). Derive WALLET_ADDRESS using xaut-trade's `swap.js` (required by prerequisites):

```bash
XAUT_SWAP=$(find -L "$HOME" -maxdepth 6 -type f -path "*/xaut-trade/scripts/swap.js" 2>/dev/null | head -1)
source ~/.aurehub/.env
WALLET_ADDRESS=$(node "$XAUT_SWAP" address | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).address")
```

If `XAUT_SWAP` is empty or the command fails, skip registration silently and continue.

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
| "buy YES on X market", "buy X at Y price", "buy shares" | buy flow |
| "sell my YES shares", "sell X shares" | sell flow |
| "browse X", "what markets", "what are the odds on X" | browse flow |
| "my polymarket balance", "how much USDC" | balance flow |
| "redeem", "claim winnings", "collect" | redeem flow |

## Browse Flow

Run environment check (no wallet, no RPC, no CLOB credentials needed):
```
node "$POLY_SCRIPTS_DIR/browse.js" "<keyword or market slug>"
```
Show the output to the user. The output includes:
- **Slug** and **ConditionId** — either can be passed as `--market` to trade.js
- **Token IDs** — for reference

Prefer passing ConditionId to `--market` when trading (more reliable than slug).

## Balance Flow

Run environment check:
```
node "$POLY_SCRIPTS_DIR/balance.js"
```

## Redeem Flow

Run environment check (no CLOB credentials needed), then:
```
node "$POLY_SCRIPTS_DIR/redeem.js"
```

Show output. If negRisk positions are skipped, tell the user to visit polymarket.com.

## Buy Flow

1. Run `node "$POLY_SCRIPTS_DIR/browse.js" <market>` to show current prices
2. Ask user: market slug, side (YES/NO), amount in USD
3. Run: `node "$POLY_SCRIPTS_DIR/trade.js" --buy --market <slug> --side YES|NO --amount <usd>`
4. The script handles approval and order submission; report the result

Pass `--dry-run` to simulate the full flow (balance checks, hard stops, order construction) without submitting any transactions.

## Sell Flow

1. Run `node "$POLY_SCRIPTS_DIR/browse.js" <market>` to confirm token IDs and current bids
2. Ask user: market slug, side (YES/NO to sell), number of shares
3. Run: `node "$POLY_SCRIPTS_DIR/trade.js" --sell --market <slug> --side YES|NO --amount <shares>`
4. The script handles setApprovalForAll and order submission; report the result

Pass `--dry-run` to simulate the full flow (balance checks, hard stops, order construction) without submitting any transactions.

## Safety Gates (handled by trade.js)

- Amount < $50: proceeds automatically
- $50 ≤ amount < $500: shows risk summary, prompts once
- Amount ≥ $500: double confirmation required
- Insufficient USDC.e (buy): auto-swap POL→USDC.e offered; swap targets 110% of needed amount (buffer), 2% slippage protection; hard-stop only if POL also insufficient
- Hard-stops: insufficient POL gas (<0.01), market CLOSED, amount < min_order_size, CTF balance insufficient (sell)

## Geo-restriction

Polymarket API blocks US and some other regions. If you see a 403 error, tell the user to enable a VPN and retry.

## Polymarket Knowledge Base

- **Chain**: Polygon mainnet (chain_id: 137)
- **Settlement currency**: USDC.e (bridged USDC, `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`)
- **Share price scale**: 0.00–1.00, where price = implied probability (e.g. $0.70 YES = 70% market probability of YES outcome)
- **Minimum share price**: $0.01; maximum: $0.99
- **Settlement**: winning shares redeem for $1.00 USDC.e each; losing shares expire worthless
- **Order type**: FOK (Fill-Or-Kill) — market orders fill immediately or cancel atomically; no partial fills left open
- **Restricted regions**: United States, United Kingdom, Singapore, and [others](https://docs.polymarket.com/polymarket-learn/FAQ/geoblocking) — use a VPN with a supported country node if blocked

Answer knowledge queries directly using the data above — no API calls needed.

## References

Load these on demand:
- `references/setup.md` — first-time setup guide
- `references/buy.md` — detailed buy flow
- `references/sell.md` — detailed sell flow
- `references/balance.md` — balance interpretation
- `references/browse.md` — browse output format
- `references/contracts.md` — Polygon contract addresses
- `references/safety.md` — safety gate details
