---
name: fomo3d
description: Play Fomo3D and Slot Machine on BNB Chain (BSC). Fomo3D is a blockchain game where players buy shares using tokens — the last buyer before the countdown ends wins the grand prize. Includes a Slot Machine mini-game with VRF-powered random spins. This skill provides a CLI to check game status, purchase shares, claim dividends, spin the slot machine, and more.
version: 1.2.0
metadata:
  openclaw:
    emoji: "🎰"
    homepage: "https://fomo3d.app"
    primaryEnv: FOMO3D_PRIVATE_KEY
    requires:
      env:
        - FOMO3D_PRIVATE_KEY
      bins:
        - node
---

# Fomo3D — BNB Chain Blockchain Game

Fomo3D is a decentralized game on BNB Chain (BSC) with two game modes:

1. **Fomo3D Main Game** — Buy shares with tokens. Each purchase resets a countdown timer. The last buyer when the timer hits zero wins the grand prize pool. All shareholders earn dividends from each purchase.

2. **Slot Machine** — Bet tokens for a VRF-powered random spin. Matching symbols win multiplied payouts (up to 100x). Depositors earn dividend shares from every spin.

## Installation and Config (required)

Ensure dependencies are installed at repo root (`npm install`).

A private key is required. If the user has not configured the skill yet, **run `fomo3d setup`** from the repo root. This runs an interactive CLI that prompts for:
- BSC private key (for signing transactions)
- Network (testnet or mainnet)
- Optional custom RPC URL

Alternatively, set environment variables (no `setup` needed):
- `FOMO3D_PRIVATE_KEY` — BSC wallet private key (hex, with or without 0x prefix)
- `FOMO3D_NETWORK` — `testnet` or `mainnet` (default: testnet)
- `FOMO3D_RPC_URL` — custom RPC endpoint (optional)

**Important:** The wallet must be an EOA (externally owned account), not a smart contract wallet. The game contracts require `msg.sender == tx.origin`.

## How to run (CLI)

Run from the **repo root** (where `package.json` lives). For machine-readable output, always append `--json`. The CLI prints JSON to stdout in `--json` mode.

```bash
fomo3d <command> [options] --json
```

On error the CLI prints `{"success":false,"error":"message"}` to stdout and exits with code 1. On success the CLI prints `{"success":true,"data":{...}}`.

## Important Concepts

### Token Amounts

All token amounts in CLI arguments and JSON output are in **wei** (18 decimals). For example:
- 1 token = `1000000000000000000` (1e18)
- 0.5 tokens = `500000000000000000` (5e17)

When displaying amounts to users, divide by 1e18 for human-readable values.

### Share Amounts

Share amounts for `purchase --shares` are **integers** (not wei). 1 share = 1 share.

### Auto-Approve

The CLI automatically checks ERC20 token allowance and approves if needed before `purchase`, `buy`, `sell`, `slot spin`, and `slot deposit`. No manual approval step required.

### FOMO Token Trading

The FOMO token is launched on the FLAP platform (BNB Chain bonding curve). Trading uses the FlapSkill contract (`0x03a9aeeb4f6e64d425126164f7262c2a754b3ff9`) which auto-routes:
- **内盘 (Portal)**: When the token is still on the bonding curve
- **外盘 (PancakeSwap V2/V3)**: After the token graduates to DEX

All trading uses **USDT** as the quote token. Buy/sell commands are only available on **mainnet**.

### VRF (Verifiable Random Function)

Slot machine spins use Binance Oracle VRF for provably fair randomness. Each `spin` requires a small BNB fee (~0.00015 BNB) sent as `msg.value`. The spin result is determined by a VRF callback (1-3 blocks later) — the CLI returns the spin request transaction, not the result. Check the result with `fomo3d slot status` or `fomo3d player` afterward.

## Commands Reference

### Setup

```bash
fomo3d setup --json
```
Interactive configuration. Prompts for private key, network, and optional RPC URL. Saves to `config.json`.

### Wallet — Check Balances

```bash
fomo3d wallet --json
```
Returns BNB balance and game token balance for the configured wallet.

**Output fields:** `address`, `bnbBalance` (wei), `tokenBalance` (wei), `tokenSymbol`, `tokenDecimals`

### Status — Game Round Info

```bash
fomo3d status --json
```
Returns current round status including countdown, prize pools, share price, and last buyers.

**Output fields:** `currentRound`, `roundStatus` (NotStarted/Active/Ended), `paused`, `countdownRemaining` (seconds), `grandPrizePool` (wei), `dividendPool` (wei), `sharePrice` (wei), `totalShares`, `lastBuyers` (address[]), `pools`

**Strategy tip:** When `countdownRemaining` is low, buying shares has higher expected value because you may win the grand prize. Each purchase resets the countdown by a fixed increment.

### Player — Player Info

```bash
fomo3d player --json
fomo3d player --address 0x1234... --json
```
Returns player's shares, earnings, and pending withdrawals. Without `--address`, uses the configured wallet.

**Output fields:** `address`, `shares`, `totalEarnings` (wei), `pendingEarnings` (wei), `pendingWithdrawal` (wei), `hasExited`, `currentRound`

**Decision guide:**
- If `pendingWithdrawal > 0`: Must run `fomo3d settle` before purchasing more shares
- If `pendingEarnings > 0` and round is active: Can `exit` to lock in earnings, or hold for more dividends
- If `hasExited == true`: Already exited this round, wait for round to end or settle

### Purchase — Buy Shares

```bash
fomo3d purchase --shares <integer> --json
```
Buy shares in the current round. The `--shares` value is an integer count (not wei). Token cost = shares × sharePrice (auto-calculated).

**Pre-checks performed automatically:**
- Game must not be paused
- No pending withdrawal (must `settle` first)
- Token approval (auto-approved if needed)

**Output fields:** `txHash`, `blockNumber`, `status`, `sharesAmount`, `tokensCost` (wei)

### Exit — Exit Game

```bash
fomo3d exit --json
```
Exit the current round and lock in your dividend earnings.

**Output fields:** `txHash`, `blockNumber`, `status`

### Settle — Claim Dividends & Prize

```bash
fomo3d settle --json
```
Settle dividends and claim any grand prize after a round ends. Must be called if `pendingEarnings > 0` or `pendingWithdrawal > 0`.

**Output fields:** `txHash`, `blockNumber`, `status`, `pendingEarnings` (wei), `pendingWithdrawal` (wei)

### End Round — End Expired Round

```bash
fomo3d end-round --json
```
End a round whose countdown has reached zero. Anyone can call this. The grand prize is distributed to the last buyer.

**Output fields:** `txHash`, `blockNumber`, `status`

### Buy — Buy FOMO with USDT (mainnet only)

```bash
fomo3d buy --amount <usdt_amount_in_wei> --json
```
Buy FOMO tokens using USDT via the FLAP platform. The FlapSkill contract auto-routes to Portal (内盘) or PancakeSwap (外盘) depending on token status. USDT allowance is auto-approved.

**Example:** Buy with 10 USDT:
```bash
fomo3d buy --amount 10000000000000000000 --json
```

**Output fields:** `txHash`, `blockNumber`, `status`, `usdtSpent` (wei), `token`

### Sell — Sell FOMO for USDT (mainnet only)

```bash
# 按数量卖出
fomo3d sell --amount <token_amount_in_wei> --json

# 按持仓比例卖出
fomo3d sell --percent <bps> --json
```
Sell FOMO tokens for USDT. Two modes:
- `--amount`: Sell exact token amount (in wei, 18 decimals)
- `--percent`: Sell by percentage of holdings in basis points (10000=100%, 5000=50%, 1000=10%)

Cannot use both flags simultaneously. Token allowance is auto-approved.

**Example:** Sell 50% of holdings:
```bash
fomo3d sell --percent 5000 --json
```

**Output fields (--amount):** `txHash`, `blockNumber`, `status`, `tokensSold` (wei), `method`
**Output fields (--percent):** `txHash`, `blockNumber`, `status`, `percentBps`, `method`

### Token Info — Token Status & Balances

```bash
fomo3d token-info --json
```
Query FOMO token status on the FLAP platform and your balances.

**Output fields (mainnet):** `token`, `network`, `status` (NotCreated/Tradable/DEX/Locked), `phase` (内盘/外盘), `quoteToken`, `currentPrice` (wei), `totalSupply` (wei), `reserveBalance` (wei), `progress` (wei), `fomoBalance` (wei), `usdtBalance` (wei), `account`

**Output fields (testnet):** `token`, `network`, `status`, `phase`, `fomoBalance` (wei), `account`

**Decision guide:**
- `status == Tradable`: Token is on 内盘 (bonding curve), buy/sell via Portal
- `status == DEX`: Token has graduated to 外盘 (PancakeSwap), buy/sell via DEX
- `progress`: How close to graduation (higher = closer to DEX)

### Slot Status — Slot Machine Info

```bash
fomo3d slot status --json
```
Returns slot machine configuration, prize pool, and statistics.

**Output fields:** `paused`, `token`, `minBet` (wei), `maxBet` (wei), `prizePool` (wei), `totalShares`, `vrfFee` (wei), `stats` { `totalSpins`, `totalBetAmount`, `totalWinAmount`, `totalDividendsDistributed` }

**Note:** `maxBet = prizePool / 100` (dynamic). If prize pool is low, max bet is low.

### Slot Spin — Spin the Slot Machine

```bash
fomo3d slot spin --bet <amount_in_wei> --json
```
Spin the slot machine. Requires token balance for the bet AND BNB for VRF fee (~0.00015 BNB).

**Constraints:**
- `minBet <= bet <= maxBet`
- Wallet must have enough BNB for VRF fee
- Cannot spin while a previous spin is pending

**Payout table:**
| Symbols | Multiplier |
|---------|-----------|
| 💎💎💎 | 100x |
| 🍒🍒🍒 | 50x |
| 🔔🔔🔔 | 50x |
| 🍋🍋🍋 | 20x |

**Output fields:** `txHash`, `blockNumber`, `status`, `betAmount` (wei), `vrfFee` (wei), `note`

**Important:** The spin result is NOT in this response. The VRF callback determines the outcome 1-3 blocks later. Check `fomo3d player --json` or `fomo3d slot status --json` afterward.

### Slot Cancel — Cancel Timed-Out Spin

```bash
fomo3d slot cancel --json
```
Cancel a spin that timed out waiting for VRF callback. Only needed if VRF fails to respond.

**Output fields:** `txHash`, `blockNumber`, `status`

### Slot Deposit — Deposit to Prize Pool

```bash
fomo3d slot deposit --amount <amount_in_wei> --json
```
Deposit tokens into the slot machine prize pool. **WARNING: Deposited tokens are permanently locked.** You receive dividend shares in return — each spin distributes 5% of the bet amount to all depositors proportionally.

**Output fields:** `txHash`, `blockNumber`, `status`, `amount` (wei)

### Slot Claim — Claim Slot Dividends

```bash
fomo3d slot claim --json
```
Claim accumulated dividends from slot machine deposits.

**Output fields:** `txHash`, `blockNumber`, `status`, `dividends` (wei)

## Recommended Workflows

### First-Time Setup

1. `fomo3d setup` — configure wallet and network
2. `fomo3d wallet --json` — verify BNB and token balances
3. `fomo3d status --json` — check game state

### Buying FOMO Tokens (mainnet)

1. `fomo3d token-info --json` — check token status and your USDT balance
2. `fomo3d buy --amount 10000000000000000000 --json` — buy with 10 USDT
3. `fomo3d token-info --json` — verify FOMO balance

### Selling FOMO Tokens (mainnet)

1. `fomo3d token-info --json` — check FOMO balance
2. `fomo3d sell --percent 5000 --json` — sell 50% of holdings
3. Or: `fomo3d sell --amount 1000000000000000000 --json` — sell exactly 1 FOMO

### Playing Fomo3D

1. `fomo3d status --json` — check round status and countdown
2. `fomo3d purchase --shares 1 --json` — buy shares (start small)
3. `fomo3d player --json` — check your earnings
4. When ready to claim: `fomo3d exit --json` then `fomo3d settle --json`
5. If countdown reaches 0 and you're the last buyer: `fomo3d end-round --json` then `fomo3d settle --json`

### Playing Slot Machine

1. `fomo3d slot status --json` — check min/max bet and prize pool
2. `fomo3d slot spin --bet <amount> --json` — spin
3. Wait 5-10 seconds for VRF callback
4. `fomo3d player --json` — check if you won

### Earning Passive Income (Slot Dividends)

1. `fomo3d slot deposit --amount <amount> --json` — deposit tokens (permanent)
2. Periodically check: `fomo3d slot claim --json` — claim dividends

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | JSON output (always use for programmatic access) |
| `--network testnet\|mainnet` | Override network |
| `--help` | Show help |
| `--version` | Show version |

## Network Info

| Network | Chain ID | Fomo3D Diamond | Slot Diamond | FOMO Token |
|---------|----------|----------------|--------------|------------|
| BSC Testnet | 97 | `0x22E309c31Bed932afB505308434fB774cB2B23a6` | `0x007813509FA42B830db82C773f0Dd243fBEbF678` | `0x57e3a4fd1fe7f837535ea3b86026916f8c7d5d46` |
| BSC Mainnet | 56 | `0x062AfaBEA853178E58a038b808EDEA119fF5948b` | `0x6eB59fFEc7CC639DFF4238D09B99Ea4c9150156E` | `0x13f26659398d7280737ffc9aba3d4f3cf53b7777` |

## Trading Contracts (mainnet only)

| Contract | Address | Purpose |
|----------|---------|---------|
| FlapSkill | `0x03a9aeeb4f6e64d425126164f7262c2a754b3ff9` | 买卖代币（自动路由内盘/外盘） |
| USDT (BSC) | `0x55d398326f99059fF775485246999027B3197955` | 支付媒介 |
| FLAP Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` | 查询代币状态 |
