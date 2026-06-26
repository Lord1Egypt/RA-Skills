# Account

## Commands

| Command | Description |
|---------|------------|
| `aiusd-core balances` | Show balances across trading, custody, staking accounts |
| `aiusd-core accounts` | Show trading account addresses per chain |
| `aiusd-core transactions [-l N]` | Show recent transactions (default: 10) |
| `aiusd-core get-deposit-address` | Show deposit addresses for all chains |

## Deposits

**Website:** https://aiusd.ai — supports multiple stablecoins, auto-converts to AIUSD

**Direct deposit** via `aiusd-core get-deposit-address`:
- Tron: **ONLY USDT** (USDC will be lost!)
- All other chains: **ONLY USDC** (USDT will be lost!)
- Minimum deposit: $10

## Staking

| Command | Description |
|---------|------------|
| `aiusd-core call genalpha_stake_aiusd -p '{"amount":"100"}'` | Stake AIUSD for yield |
| `aiusd-core call genalpha_unstake_aiusd -p '{"amount":"50"}'` | Unstake (3-day lock) |
| `aiusd-core call genalpha_withdraw_to_wallet -p '{"amount":"100","chain_id":"solana:mainnet-beta"}'` | Withdraw stablecoins to wallet |

## Gas Top-up

| Command | Description |
|---------|------------|
| `aiusd-core call genalpha_ensure_gas -p '{"chain_id":"solana:mainnet-beta"}'` | Top up native gas using AIUSD |
