---
name: likwid-fi
version: 1.0.0
description: Likwid.fi Protocol Universal Skill — swap, liquidity, margin, and lending on the Likwid DeFi protocol.
homepage: https://likwid.fi
---

# Likwid.fi Protocol Universal Skill

Interact with the **Likwid Protocol** — a unified DeFi protocol for swaps, liquidity provision, margin trading, and lending. Works with any EOA wallet or ERC-4337 Smart Account.

## Skill Architecture

| File | Purpose |
|------|---------|
| **SKILL.md** (this file) | Skill documentation and agent workflow |
| **likwid-fi.js** | CLI implementation |
| **package.json** | Dependencies (viem, permissionless) |
| **bootstrap.sh** | One-line install script |
| **abi/** | On-chain contract ABIs |
| **pools/** | Per-network pool & contract configuration |

## Supported Networks

| Network | Config File |
|---------|-------------|
| Base (mainnet) | `pools/base.json` |
| Ethereum (mainnet) | `pools/ethereum.json` *(coming soon)* |
| Sepolia (testnet) | `pools/sepolia.json` *(legacy)* |

---

## 0. First Load — Setup

**When this skill is first loaded**, you MUST run the bootstrap and configure it before any DeFi operation. Do NOT silently proceed.

### Fast Path (preferred)

If the skill is already installed locally, reuse it immediately:

```bash
test -f ~/.openclaw/skills/agent-genesis/likwid-fi/likwid-fi.js && echo "skill present"
```

### Standard Install / Update

Run the bootstrap script to install or update everything in one shot:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/likwid-fi/bootstrap.sh)
```

After bootstrap, all commands run from `~/.openclaw/skills/agent-genesis/likwid-fi/`.

### Step 1: Interactive Setup

After bootstrap completes, ask the user for three things:

1. **Network** — Which network to operate on?
   > Available: `base`, `sepolia`, `ethereum`

2. **Private Key File** — Where is your wallet's private key stored?
   > Provide the **file path** containing the private key (hex string, with or without `0x` prefix).
   > Also supports JSON wallet files with a `privateKey` field.
   >
   > **NEVER** ask the user to paste their private key directly. Always ask for the **file path**.

Then run:

```bash
node likwid-fi.js setup <network> <keyFilePath>
```

Gas mode is auto-detected: if the network has a Paymaster configured, gas is paid in AGC via Smart Account (EIP-7702). Otherwise, direct EOA transactions pay gas in ETH. Use `LIKWID_NO_PAYMASTER=1` env var to force direct ETH mode.

**Report to human:**

> **Likwid.fi Skill Configured!**
>
> Network: `<NETWORK>` (Chain ID `<CHAIN_ID>`)
> Address: `<ADDRESS>`
> Gas Mode: `Paymaster (AGC)` or `Direct (ETH)`
>
> **CRITICAL:** Your private key is read from `<KEY_FILE>`. Never share this file.

### Step 3: Verify Account

```bash
node likwid-fi.js account
```

Show the user their balances and addresses.

---

## 1. Swap

Swap tokens on any Likwid pool.

### Step 1: List Available Pools

```bash
node likwid-fi.js pools
```

**Report to human:**

> **Available Pools on `<NETWORK>`:**
>
> ETH/USDT (fee: 0.30%)
> ETH/LIKWID (fee: 0.30%)
> ETH/LIKWID (fee: 0.50%)
>
> Which pool and direction?

### Step 2: Get Quote

Before executing, always preview the swap:

```bash
node likwid-fi.js quote <pool> <direction> <amount>
```

**Direction (Exact Input — sell specific amount):**
- `sell0` — Sell currency0 for currency1 (e.g., sell 0.001 ETH → get ~X AGC)
- `sell1` — Sell currency1 for currency0 (e.g., sell 100 AGC → get ~X ETH)

**Direction (Exact Output — buy specific amount):**
- `buy1` — Buy exact amount of currency1 (e.g., buy 100 AGC → cost ~X ETH)
- `buy0` — Buy exact amount of currency0 (e.g., buy 0.001 ETH → cost ~X AGC)

**Examples:**
```bash
node likwid-fi.js quote ETH/AGC sell0 0.001    # sell 0.001 ETH, get ~? AGC
node likwid-fi.js quote ETH/AGC buy1 100       # buy 100 AGC, cost ~? ETH
node likwid-fi.js quote ETH/AGC sell1 100      # sell 100 AGC, get ~? ETH
node likwid-fi.js quote ETH/AGC buy0 0.001     # buy 0.001 ETH, cost ~? AGC
```

**Report to human (exact input):**

> **Swap Preview:**
> Swapping `<AMOUNT>` `<FROM>` → ~`<OUTPUT>` `<TO>`
> Fee: `<FEE_RATE>`% (`<FEE_AMOUNT>` `<FROM>`)
> Slippage tolerance: `<SLIPPAGE>`%
>
> Proceed? (yes/no)

**Report to human (exact output):**

> **Swap Preview (Exact Output):**
> Buying `<AMOUNT>` `<TO>` → cost ~`<COST>` `<FROM>`
> Fee: `<FEE_RATE>`% (`<FEE_AMOUNT>` `<FROM>`)
> Max cost (`<SLIPPAGE>`% slippage): `<MAX_COST>` `<FROM>`
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

### Step 3: Execute Swap

```bash
node likwid-fi.js swap <pool> <direction> <amount> [slippage%]
```

Default slippage: 1%. For exact output swaps, slippage is applied to the max input cost.

**Report to human:**

> **Swap Successful!**
> `<AMOUNT>` `<FROM>` → `<TO>`
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

Or on failure:

> **Swap Failed:** `<ERROR_MESSAGE>`
> No funds were spent.

---

## 2. Add / Increase Liquidity

Provide liquidity to a Likwid pool. If you already have a position in the pool, the command automatically uses `increaseLiquidity` (adds to the existing NFT). Otherwise it creates a new LP position (ERC-721 NFT) via `addLiquidity`.

### Step 1: Select Pool & Check State

```bash
node likwid-fi.js pool_info <pool>
```

**If pool is not initialized:**

> **Pool Not Initialized**
> Pool `<NAME>` (fee: `<FEE>`%) has no liquidity. You need to Create a Pair first.

**If pool exists, report to human:**

> **Pool `<NAME>` (fee: `<FEE>`%)**
> Reserve `<SYMBOL0>`: `<RESERVE0>`
> Reserve `<SYMBOL1>`: `<RESERVE1>`
> Rate: 1 `<SYMBOL0>` = `<RATE>` `<SYMBOL1>`
>
> How much liquidity would you like to add? You can provide an amount for either `<SYMBOL0>` or `<SYMBOL1>` — the other side will be auto-calculated from the pool ratio.

### Step 2: Execute

The user provides an amount for **one side** (currency `0` or `1`). The matching amount is auto-calculated.

```bash
node likwid-fi.js lp_add <pool> <currency> <amount> [slippage%]
```

- `<currency>`: `0` for currency0, `1` for currency1
- The other side is calculated proportionally from the on-chain reserve ratio
- Existing positions are auto-detected via the Likwid API. If found, `increaseLiquidity` is used with the existing `tokenId`.

**Report to human before execution:**

> **Add Liquidity Preview:** (or **Increase Liquidity Preview** if existing position found)
> Pool: `<NAME>` (fee: `<FEE>`%)
> Rate: 1 `<SYMBOL0>` = `<RATE>` `<SYMBOL1>`
> `<SYMBOL0>`: `<AMOUNT0>`
> `<SYMBOL1>`: `<AMOUNT1>`
> Slippage: `<SLIPPAGE>`%
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

**After execution:**

> **Liquidity Added!** (or **Liquidity Increased!**)
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

Or on failure:

> **Add Liquidity Failed:** `<ERROR_MESSAGE>`
> No funds were spent.

---

## 2b. View Liquidity Positions

View your LP positions in a specific pool.

```bash
node likwid-fi.js lp_positions <pool>
```

**Report to human:**

> **Your Liquidity Positions:**
>
> Pool: `<NAME>`  Swap Fee: `<FEE>`%  Margin Fee: `<MARGIN_FEE>`%
> Your Pool Share: `<SHARE>`%
> `<SYMBOL0>`: `<AMOUNT0>`
> `<SYMBOL1>`: `<AMOUNT1>`
>
> Tip: Use "lp_add" to increase liquidity, or "lp_remove" to remove liquidity.

If no positions found:

> No liquidity positions found for `<NAME>`.

---

## 2c. Remove Liquidity

Remove liquidity from an existing LP position.

### Step 1: Check Position

```bash
node likwid-fi.js lp_positions <pool>
```

Report the user's current position details (pool share, token amounts).

### Step 2: Execute

```bash
node likwid-fi.js lp_remove <pool> [percentage]
```

- `[percentage]`: 1-100 (default: 100 = remove all liquidity)
- The first position in the pool is used automatically

**Report to human before execution:**

> **Remove Liquidity Preview:**
> Pool: `<NAME>` (fee: `<FEE>`%) — tokenId: `<TOKEN_ID>`
> Removing: `<PERCENT>`% of liquidity
> Est. `<SYMBOL0>`: `<AMOUNT0>`
> Est. `<SYMBOL1>`: `<AMOUNT1>`
> Slippage: 1%
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

**After execution:**

> **Liquidity Removed!**
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

Or on failure:

> **Remove Liquidity Failed:** `<ERROR_MESSAGE>`
> No funds were withdrawn.

---

## 3. Create a Pair

Create a new Likwid pool by initializing it on-chain. Tokens are resolved by name from the network config.

### Step 1: Check Available Tokens

```bash
node likwid-fi.js pools
```

The tokens available for pairing are defined in `pools/<network>.json` under `tokens`. Current Base tokens: ETH, USDC, AGC.

### Step 2: Create the Pair

```bash
node likwid-fi.js create_pair <token0> <token1> <fee> <marginFee>
```

- `<token0>`, `<token1>`: Token names (e.g., `ETH`, `USDT`). Addresses are auto-sorted to satisfy `currency0 < currency1`.
- `<fee>`, `<marginFee>`: Fee values in basis points (e.g., `3000` = 0.30%).

**Report to human:**

> **Create Pair Preview:**
> currency0: `<SYMBOL0>` (`<ADDRESS0>`)
> currency1: `<SYMBOL1>` (`<ADDRESS1>`)
> Swap Fee: `<FEE>`%  Margin Fee: `<MARGIN_FEE>`%
> Pool ID: `<POOL_ID>`
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

**On success:**

> **Pair Created!**
> Pool added to config: `<NAME>` (fee: `<FEE>`%).
> Use `lp_add <NAME> <currency> <amount>` to add initial liquidity.

**If pool already exists:**

> **Pool Already Exists**
> This pair is already initialized on-chain. Use `pools` to check if it's in your config, or `lp_add` to add liquidity.

---

## 4. Margin Trading

Open leveraged long/short positions on Likwid pools.

### Understanding Direction

For pool `ETH/LIKWID` (currency0=ETH, currency1=LIKWID):

| Direction | Meaning | Collateral | Borrow |
|---|---|---|---|
| `long` | Long LIKWID (Short ETH) | LIKWID | ETH |
| `short` | Short LIKWID (Long ETH) | ETH | LIKWID |

Direction is always relative to **currency1**. `long` = bullish on currency1, `short` = bearish on currency1.

### Step 1: Get Quote

Always preview before opening a position:

```bash
node likwid-fi.js margin_quote <pool> <direction> <leverage> <amount>
```

Example:
```bash
node likwid-fi.js margin_quote ETH/LIKWID short 1 0.1
```

**Report to human:**

> **Margin Preview: Short LIKWID (Long ETH) | ETH/LIKWID | 1x**
>
> Margin: `0.1 ETH`
> Total (Using Margin 1x): `0.0997 ETH`
> Borrow Amount: `980.73 LIKWID`
> Borrow APY: `5.00%`
>
> Initial Margin Level: `2.00`
> Liquidation Margin Level: `1.17`
> Liq.Price: `0.00017404 ETH per LIKWID`
>
> Max Margin (1x): `1.506 ETH`
> Borrow Max Amount: `990.54 LIKWID` (includes 1% slippage)
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

### Step 2: Open / Increase Position

```bash
node likwid-fi.js margin_open <pool> <direction> <leverage> <amount>
```

The command automatically:
1. Queries the API for existing margin positions on the same pool
2. If an existing position with the same direction exists → **increases** it (`margin()`)
3. If no position exists → **opens** a new one (`addMargin()`)

**After execution:**

> **Margin Position Opened!**
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

Or on failure:

> **Margin Open Failed:** `<ERROR_MESSAGE>`
> No funds were spent.

### Leverage & Max Margin

| Leverage | Max Margin Ratio |
|---|---|
| 1x | 15% of pairReserve (capped by realReserve) |
| 2x | 12% |
| 3x | 9% |
| 4x | 5% |
| 5x | 1.7% |

Higher leverage = smaller max position, higher liquidation risk.

### Step 3: View Positions

```bash
node likwid-fi.js margin_positions <pool>
```

Shows all your margin positions on the given pool with real-time on-chain data.

**Report to human:**

> **Margin Positions: ETH/LIKWID** (Swap Fee: 0.30% Margin Fee: 0.30%)
> Current Price: `0.00010066 ETH per LIKWID`
>
> **Position #20**
> Short LIKWID · Long ETH
> Margin Amount: `0.001 ETH`
> Margin Total: `0.000997 ETH`
> Debt: `9.9654 LIKWID`
> Borrow APY: `5.00%`
> Liq.Price: `0.00018217 ETH`
> Cur.Price: `0.00010066 ETH`
> Margin Level: `1.99`
> Estimated PNL: `-0.00000902 ETH`

Data source: API provides `tokenId` only; all other data (marginAmount, marginTotal, debtAmount, direction) is read on-chain via `getPositionState()`.

**PNL Calculation:**
- If debt currency ≠ price currency: `PNL = marginTotal - (debt × curPrice)`
- If debt currency = price currency: `PNL = marginTotal - (debt × 1/curPrice)`

### Step 4: Close Position

Close all or part of a margin position. Supports partial closing (e.g., 50%).

#### 4a. Ask the User

Before running anything, collect from the user:

1. **Pool** — Which pool? (e.g., ETH/LIKWID)
2. **Direction** — Which side to close? `long` (Long currency1) or `short` (Short currency1)
3. **Close Percentage** — How much to close? 1-100%

#### 4b. Query Positions

Run `margin_positions` to find the user's open positions in that pool and direction:

```bash
node likwid-fi.js margin_positions <pool>
```

Filter the results by the requested direction (`long` or `short`).

- **No positions found →** Tell the user: "You have no open `<DIRECTION>` positions on `<POOL>`."
- **One position →** Proceed automatically with that tokenId.
- **Multiple positions →** Show all matching positions to the user and ask which tokenId to close:

> **Found 3 Long LIKWID positions on ETH/LIKWID:**
>
> `#20` — Margin: 3 LIKWID, Total: 5.982 LIKWID, Debt: 0.00060581 ETH
> `#25` — Margin: 1 LIKWID, Total: 1.994 LIKWID, Debt: 0.00020193 ETH
> `#31` — Margin: 5 LIKWID, Total: 9.970 LIKWID, Debt: 0.00101000 ETH
>
> Which position to close? (enter tokenId)

**Wait for user selection before proceeding.**

#### 4c. Preview (margin_close_quote)

Use `margin_close_quote` to preview without executing:

```bash
node likwid-fi.js margin_close_quote <pool> <tokenId> <percent> [slippage%]
```

**Example:**
```bash
node likwid-fi.js margin_close_quote ETH/LIKWID 20 50
```

**Close Calculation:**
- `releaseAmount = (marginAmount + marginTotal) × closeScale`
- `costAmount = LikwidHelper.getAmountIn(!marginForOne, debt × closeScale, dynamicFee=false)`
- `closeAmount = releaseAmount - costAmount`
- `PNL = closeAmount - marginAmount × closeScale`
- `closeAmountMin = closeAmount × (1 - slippage)`

**Report to human:**

> **Margin Close Preview**
> Pool: ETH/LIKWID Swap Fee: 0.3% Margin Fee: 0.3%
> Long LIKWID (Short ETH)
> Position #20
>
> Margin Amount: `3 LIKWID`
> Margin Total: `5.982 LIKWID`
> Debt: `0.00060581 ETH`
> Liq.Price: `0.00018217 ETH`
> Cur.Price: `0.00018317 ETH`
> Margin Level: `1.99`
>
> --- Close Scale 50% ---
> Close Debt: `0.00030290 ETH`
> Estimated PNL: `-0.02699081 LIKWID`
> Max Slippage: `1%`
> Min. Received: `1.46564415 LIKWID`
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

#### 4d. Execute (margin_close)

On confirmation, execute with the same parameters:

```bash
node likwid-fi.js margin_close <pool> <tokenId> <percent> [slippage%]
```

**Example:**
```bash
node likwid-fi.js margin_close ETH/LIKWID 20 50
```

On-chain contract call: `close(tokenId, closeMillionth, closeAmountMin, deadline)`
- `closeMillionth = percent × 10000` (e.g., 50% → 500000, 100% → 1000000)

**Report to human:**

> **Margin Close Successful!**
> Position #`<TOKEN_ID>` closed `<PERCENT>`%
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

Or on failure:

> **Margin Close Failed:** `<ERROR_MESSAGE>`
> Position was NOT modified.

**Key notes:**
- Partial close (e.g., 50%) keeps the remaining position open with reduced margin and debt.
- 100% close fully repays debt and returns remaining margin to the user.
- `InsufficientCloseReceived` error means the position may be near liquidation — the swap output cannot cover the debt.

### Step 5: Repay Debt

Repay part or all of the borrow debt on a margin position. This reduces leverage and releases proportional margin back to you.

#### 5a. Ask the User

Collect from the user:

1. **Pool** — Which pool? (e.g., ETH/LIKWID)
2. **tokenId** — Which position? (use `margin_positions` to find it)
3. **Amount** — How much debt to repay? (in borrow currency, capped at current debt)

#### 5b. Preview (margin_repay_quote)

```bash
node likwid-fi.js margin_repay_quote <pool> <tokenId> <amount>
```

**Example:**
```bash
node likwid-fi.js margin_repay_quote ETH/LIKWID 20 0.0003
```

**Report to human:**

> **Margin Repay Preview**
> Pool: ETH/LIKWID Swap Fee: 0.3% Margin Fee: 0.3%
> Long LIKWID (Short ETH)
> Position #20
>
> Margin Amount: `3 LIKWID`
> Margin Total: `5.982 LIKWID`
> Debt: `0.00060581 ETH`
> Cur.Price: `0.00018317 ETH per LIKWID`
>
> --- Repay ---
> Repay Amount: `0.0003 ETH`
> Release: `~4.446 LIKWID`
> Debt After: `0.00030581 ETH`
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

**Key notes:**
- If the user enters more than the current debt, it is automatically capped at the debt amount.
- Repaying with native ETH sends value directly. Repaying with ERC-20 requires approval first (handled automatically).

#### 5c. Execute (margin_repay)

```bash
node likwid-fi.js margin_repay <pool> <tokenId> <amount>
```

On-chain contract call: `repay(tokenId, repayAmount, deadline)` (payable — sends ETH if borrow currency is native).

**Report to human:**

> **Margin Repay Successful!**
> Position #`<TOKEN_ID>` — repaid `<AMOUNT>` `<BORROW_TOKEN>`
> Transaction: `<TX_HASH>`
> Block: `<BLOCK_NUMBER>`

### Step 6: Adjust Margin (Modify)

Increase or decrease the margin collateral on an existing position without changing leverage or debt.

- **Increase**: Adds margin → raises margin level → reduces liquidation risk
- **Decrease**: Removes margin → lowers margin level → must stay above 1.4

#### 6a. Ask the User

Collect from the user:

1. **Pool** — Which pool? (e.g., ETH/LIKWID)
2. **tokenId** — Which position? (use `margin_positions` to find it)
3. **Change Amount** — Positive to increase, negative to decrease (e.g., `0.5` or `-0.5`)

#### 6b. Preview (margin_modify_quote)

```bash
node likwid-fi.js margin_modify_quote <pool> <tokenId> <changeAmount>
```

**Examples:**
```bash
node likwid-fi.js margin_modify_quote ETH/LIKWID 20 1.0     # increase by 1 LIKWID
node likwid-fi.js margin_modify_quote ETH/LIKWID 20 -0.5    # decrease by 0.5 LIKWID
```

**Report to human (decrease example):**

> **Margin Modify Preview**
> Pool: ETH/LIKWID Swap Fee: 0.3% Margin Fee: 0.3%
> Long LIKWID (Short ETH)
> Position #20
>
> Margin Amount: `3 LIKWID`
> Margin Total: `5.982 LIKWID`
> Debt: `0.00060581 ETH`
> Cur.Price: `0.00018317 ETH per LIKWID`
> Margin Level: `1.99`
>
> --- Decrease Margin ---
> Decrease Amount: `0.5 LIKWID`
> Decrease Max: `2.742 LIKWID` (min level: 1.4)
> New Margin Level: `1.88`
>
> Proceed? (yes/no)

**Wait for human confirmation before executing.**

**Key notes:**
- Decrease amount is automatically capped at the max allowed (to maintain margin level >= 1.4).
- Decrease max formula: `(marginAmount + marginTotal) - 1.4 × debtValueInMarginCurrency`
- After execution, the updated margin level is displayed.

#### 6c. Execute (margin_modify)

```bash
node likwid-fi.js margin_modify <pool> <tokenId> <changeAmount>
```

On-chain contract call: `modify(tokenId, changeAmount, deadline)` (payable for increase with native ETH).

**Report to human:**

> **Margin Modify Successful!**
> Position #`<TOKEN_ID>` — `<INCREASED/DECREASED>` `<AMOUNT>` `<MARGIN_TOKEN>`
> Updated Margin Level: `<NEW_LEVEL>`
> Transaction: `<TX_HASH>`

---

## 5. Error Handling

When errors occur, **always inform the human clearly**. Never silently swallow errors.

| Error Type | What to Tell the Human |
|---|---|
| **Not configured** | "Run setup first: `node likwid-fi.js setup <network> <keyFile>`" |
| **Key file not found** | "Private key file not found at `<PATH>`. Please check the path." |
| **Pool not found** | "Pool `<NAME>` not found. Use token pair (e.g. ETH/USDT). Run `pools` to list." |
| **Quote failed** | "Could not get quote — pool may have insufficient liquidity." |
| **Approval failed** | "Token approval failed. Swap was NOT executed." |
| **Swap reverted** | "Swap transaction reverted. No funds were lost. Check slippage or try a smaller amount." |
| **Insufficient balance** | "Insufficient `<TOKEN>` balance. You have `<BALANCE>`, need `<REQUIRED>`." |
| **UserOp failed** | "Smart Account UserOperation failed: `<REASON>`. Falling back to direct transaction." |

**Key principle:** If a multi-step operation fails at any step (e.g., approval fails before swap), **stop immediately** and report.

---

## 6. All Commands Reference

| Command | Description |
|:---|:---|
| `setup <net> <key>` | Configure network and wallet. Gas mode auto-detected. |
| `account` | Show current account info and balances. |
| `pools` | List available pools on the current network. |
| `pool_info <pool>` | Query on-chain pool state (reserves, rate). |
| `quote <pool> <dir> <amt>` | Get swap output estimate without executing. |
| `swap <pool> <dir> <amt> [slip]` | Execute a swap. |
| `lp_add <pool> <cur> <amt> [slip]` | Add or increase liquidity. `<cur>`: `0` or `1`. |
| `lp_positions <pool>` | Show your liquidity positions in a pool. |
| `lp_remove <pool> [percent]` | Remove liquidity. Default: 100% (all). |
| `create_pair <t0> <t1> <fee> <mfee>` | Create a new pool. Tokens by name. |
| `margin_quote <pool> <dir> <lev> <amt>` | Preview margin position. |
| `margin_open <pool> <dir> <lev> <amt>` | Open or increase margin position. |
| `margin_positions <pool>` | Show your margin positions. |
| `margin_close_quote <pool> <id> <pct> [slip]` | Preview margin close. |
| `margin_close <pool> <id> <pct> [slip]` | Execute margin close. |
| `margin_repay_quote <pool> <id> <amt>` | Preview margin repay. |
| `margin_repay <pool> <id> <amt>` | Execute margin repay. |
| `margin_modify_quote <pool> <id> <chg>` | Preview margin adjust. |
| `margin_modify <pool> <id> <chg>` | Execute margin adjust (+increase/-decrease). |

### Arguments

| Arg | Values | Description |
|:---|:---|:---|
| `<net>` | `base`, `sepolia`, `ethereum` | Target network. |
| `<key>` | File path | Path to file containing private key. |
| `<pool>` | `ETH/USDT`, `ETH-LIKWID` | Token pair. Lowest fee tier selected by default. |
| `<dir>` | `sell0`, `sell1`, `buy0`, `buy1` | Swap direction. `sell0`/`sell1` = exact input, `buy0`/`buy1` = exact output. |
| `<cur>` | `0`, `1` | Which currency to provide (other auto-calculated). |
| `<amt>` | `"0.01"`, `"100"` | Human-readable token amount. |
| `[slip]` | `1`, `0.5`, `3` | Slippage tolerance in % (default: `1`). |
| `<t0>`, `<t1>` | `ETH`, `USDT`, ... | Token names from network config `tokens`. |
| `<fee>`, `<mfee>` | `3000` | Fee in basis points (3000 = 0.30%). |
| `<dir>` (margin) | `long`, `short` | Direction relative to currency1. |
| `<lev>` | `1`-`5` | Leverage multiplier. |
| `<pct>` | `1`-`100` | Close percentage (e.g., 50 = close half). |

---

## 7. Adding New Networks

To add a new network, create a JSON file in `pools/<network>.json`:

```json
{
  "network": "<name>",
  "chainId": "<id>",
  "rpc": "<rpc_url>",
  "bundlerUrl": "<bundler_url>",
  "paymaster": "<paymaster_address>",
  "contracts": {
    "LikwidVault": "<address>",
    "LikwidPairPosition": "<address>",
    "LikwidMarginPosition": "<address>",
    "LikwidLendPosition": "<address>",
    "LikwidHelper": "<address>"
  },
  "tokens": {
    "ETH": { "address": "0x0000000000000000000000000000000000000000", "decimals": 18 },
    "USDT": { "address": "<addr>", "decimals": 6 }
  },
  "pools": {
    "ETH/USDT": [
      {
        "currency0": { "address": "<addr>", "symbol": "ETH", "decimals": 18 },
        "currency1": { "address": "<addr>", "symbol": "USDT", "decimals": 6 },
        "fee": 3000,
        "marginFee": 3000
      }
    ]
  }
}
```

Then switch to the new network:
```bash
node likwid-fi.js setup <new_network> <keyFile>
```
