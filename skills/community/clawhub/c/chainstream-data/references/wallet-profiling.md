# Wallet Profiling Reference

## CLI Commands → REST API Mapping

| CLI Command | REST Endpoint | Method |
|-------------|--------------|--------|
| `wallet profile --chain sol --address ADDR` | Multiple: `/pnl` + `/net-worth` + `/tokens-balance` | GET (aggregated) |
| `wallet pnl --chain sol --address ADDR` | `GET /v2/wallet/sol/ADDR/pnl` | GET |
| `wallet holdings --chain sol --address ADDR` | `GET /v2/wallet/sol/ADDR/tokens-balance` | GET |
| `wallet activity --chain sol --address ADDR` | `GET /v2/wallet/sol/ADDR/transfers` | GET |

## All Wallet Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v2/wallet/{chain}/{walletAddress}/pnl` | PnL summary (realized + unrealized) |
| POST | `/v2/wallet/{chain}/{walletAddress}/calculate-pnl` | Trigger async PnL recalculation |
| GET | `/v2/wallet/{chain}/{walletAddress}/pnl-details` | Detailed PnL breakdown |
| GET | `/v2/wallet/{chain}/{walletAddress}/pnl-by-token` | PnL per token held |
| GET | `/v2/wallet/{chain}/{walletAddress}/net-worth` | Total net worth in USD |
| GET | `/v2/wallet/{chain}/{walletAddress}/net-worth-chart` | Net worth over time |
| GET | `/v2/wallet/{chain}/{walletAddress}/tokens-balance` | Current token balances |
| GET | `/v2/wallet/{chain}/{walletAddress}/transfers` | Transfer history |
| GET | `/v2/wallet/{chain}/{walletAddress}/balance-updates` | Recent balance changes |

## Wallet Profiling Workflow

### Step 1: Overview

```bash
npx @chainstream-io/cli wallet profile --chain sol --address <addr>
```

Returns PnL + net worth + top holdings in one call.

### Step 2: Behavior analysis

From the profile data, assess:

| Metric | Interpretation |
|--------|---------------|
| **Win rate** | Realized PnL > 0 trades / total trades |
| **Holding period** | Short (< 1h) = scalper, Medium (1h-1d) = swing, Long (> 1d) = holder |
| **Concentration** | Top holding as % of net worth. > 50% = concentrated risk |
| **Activity frequency** | Transfers per day. > 50 = active trader |
| **Token diversity** | Number of unique tokens held. < 5 = focused, > 20 = diversified |

### Step 3: Deep dive on top holdings

```bash
npx @chainstream-io/cli token info --chain sol --address <top_token_address>
npx @chainstream-io/cli token security --chain sol --address <top_token_address>
```

### PnL Interpretation

- `realizedPnl`: Profit/loss from closed positions (sold tokens)
- `unrealizedPnl`: Paper profit/loss on current holdings
- `totalPnl`: `realizedPnl + unrealizedPnl`
- Values in USD. Negative = loss.
