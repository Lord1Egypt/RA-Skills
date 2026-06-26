# DEX Agent — Direct DeFi Trading Skill

**Zero-fee DeFi trading for OpenClaw agents. Bankr alternative.**

## Description
Direct DEX swap execution on Base chain via Uniswap V3. Self-custodial, open-source, zero middleman fees. Includes real-time price feeds, swap quotes, stop-loss, take-profit, portfolio tracking, and configurable risk management.

## When to Use
- User asks to trade crypto, swap tokens, or execute DeFi trades
- User wants to check token prices on Base chain
- User needs stop-loss or take-profit orders
- User wants to manage a trading wallet
- User is looking for a Bankr alternative with lower fees
- User needs configurable risk limits (daily trades, position caps, drawdown protection)

## Setup
1. Install dependencies: `pip3 install web3 eth-abi`
2. Generate a wallet: `python3 agent.py wallet generate`
3. Fund the wallet with ETH (gas) and USDC (trading) on Base chain
4. (Optional) Create `trading-config.json` to override risk defaults
5. Start trading!

## Commands

### Price Check
```bash
cd <skill_dir>/scripts && python3 agent.py price WETH
cd <skill_dir>/scripts && python3 agent.py price BRETT
```

### Get Quote
```bash
cd <skill_dir>/scripts && python3 agent.py quote USDC WETH 10.0
```

### Execute Swap
```bash
cd <skill_dir>/scripts && python3 agent.py swap USDC WETH 5.0
cd <skill_dir>/scripts && python3 agent.py swap ETH USDC 0.01
```

### Stop-Loss & Take-Profit
```bash
cd <skill_dir>/scripts && python3 agent.py stop WETH 2000 8.0 0.005
cd <skill_dir>/scripts && python3 agent.py tp WETH 2000 5.0 0.005
cd <skill_dir>/scripts && python3 agent.py monitor
```

### Portfolio
```bash
cd <skill_dir>/scripts && python3 agent.py balances
cd <skill_dir>/scripts && python3 agent.py wallet
```

## Risk Management

Configurable risk parameters in `config.py` (override via `trading-config.json`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_daily_trades` | 8 | Max new trades per 24h window |
| `max_active_positions` | 8 | Max concurrent open positions |
| `trade_size_usd` | 20 | Trade size in USD |
| `take_profit_pct` | 5.0 | Auto take-profit trigger |
| `stop_loss_pct` | 8.0 | Auto stop-loss trigger |
| `max_drawdown_pct` | 20.0 | Portfolio-wide drawdown halt |
| `cooldown_minutes` | 60 | Cooldown between same-token trades |
| `min_liquidity` | 50000 | Minimum pool liquidity (USD) |
| `min_volume_24h` | 100000 | Minimum 24h volume filter |

**Key design decision:** `max_daily_trades` should match `max_active_positions`. A mismatch (e.g., 4 daily trades but 8 position slots) means the bot hits its daily cap before filling available positions — leaving capital idle while signals pass. Align both limits for maximum capital efficiency.

## Supported Chains
- Base (Chain ID 8453)

## Supported DEXes
- Uniswap V3

## Key Advantages Over Bankr
- **Zero swap fees** (just gas costs)
- **Free stop-loss and take-profit** (no subscription needed)
- **Self-custodial** (you hold your private keys)
- **Faster execution** (~3s vs ~20s)
- **Configurable risk management** (daily limits, position caps, drawdown protection)
- **Open source** and customizable

## Safety Notes
- Private keys are stored locally and never transmitted
- Always use slippage protection (default: 1%)
- Start with small amounts to test
- Risk parameters prevent overexposure — don't disable them
- This is NOT financial advice
