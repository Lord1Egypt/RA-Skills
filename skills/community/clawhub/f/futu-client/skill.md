# Futu API Skill

## Overview

The futu-client skill provides a convenient client for querying stock positions, account info, placing orders, and more using Futu OpenAPI. It wraps the `futu` (futu-api) library to offer a simplified interface for trading and querying.

## Features

### Requirements
- **FutuOpenD** must be running on `127.0.0.1:11111`
- Install dependencies: `pip install futu-api`

### Supported Markets
- **HK Stocks**: Codes like "HK.00700" (Tencent), "HK.01810" (Xiaomi)
- **US Stocks**: Codes like "US.AAPL", "US.QQQ"
- **CN Stocks**: Codes like "SH.600000", "SZ.000001"

### Data Types

| Category | Methods |
|----------|---------|
| **Positions** | `get_positions` - Get current positions |
| **Account** | `get_account_info` - Get account balance, buying power |
| **Trading** | `place_order`, `modify_order`, `unlock_trade` |
| **Orders** | `get_orders` - Today's orders |
| **Deals** | `get_today_deals` - Today's executed trades |
| **History** | `get_history_orders`, `get_history_deals` |
| **Watchlists** | `get_watchlist`, `get_all_watchlists` - Get self-selected stocks |
| **Quotes** | `get_quote`, `get_market_snapshot` |
| **Trading Info** | `get_max_tradable_qty` |

## Usage

### Installation

```bash
pip install futu-api pandas
```

Note: FutuOpenD must be running on your machine before using this skill.

### Basic Usage

```python
from futu_client import FutuClient
from futu import TrdSide, OrderType, TrdEnv

# Create client
client = FutuClient()

# Get positions
positions = client.get_positions(trd_env=TrdEnv.REAL)
print(positions)

# Get account info
account = client.get_account_info()
print(f"Total assets: {account['total_assets']}")
print(f"Buying power: {account['power']}")

# Get today's deals
deals = client.get_today_deals()
print(deals)

# Place an order (for real trading, use TrdEnv.REAL)
# result = client.place_order(
#     price=100.0,
#     qty=100,
#     code="HK.00700",
#     trd_side=TrdSide.BUY,
#     trd_env=TrdEnv.SIMULATE  # Use SIMULATE for testing
# )

# Get quote
quote = client.get_quote("US.AAPL")
print(f"AAPL price: {quote['last_price']}")

client.close()
```

### Key Methods

#### get_positions(trd_env=TrdEnv.REAL)
Returns current positions as a DataFrame with columns:
- `code`: Stock code
- `stock_name`: Stock name
- `qty`: Position quantity
- `can_sell_qty`: Available to sell
- `cost_price`: Cost price
- `nominal_price`: Current market price
- `pl_ratio`: Profit/loss ratio (%)
- `currency`: Currency (HKD, USD, etc.)

#### get_account_info(trd_env=TrdEnv.REAL)
Returns account information as a dictionary:
- `total_assets`: Total assets
- `cash`: Available cash
- `power`: Buying power
- `market_val`: Position market value
- `currency`: Account currency

#### place_order(price, qty, code, trd_side, order_type, trd_env)
Place an order. Returns order result.

Parameters:
- `price`: Order price (float)
- `qty`: Order quantity (int)
- `code`: Stock code (e.g., "HK.00700", "US.AAPL")
- `trd_side`: TrdSide.BUY or TrdSide.SELL
- `order_type`: OrderType.NORMAL (default)
- `trd_env`: TrdEnv.REAL (real) or TrdEnv.SIMULATE (paper trading)

#### get_quote(code)
Get real-time quote for a stock.

#### get_market_snapshot(codes)
Get market snapshot for multiple stocks.

#### get_watchlist(group_name="全部")
Get user's watchlist (self-selected stocks).

Parameters:
- `group_name`: Watchlist group name. Common values:
  - "全部" (All) - default
  - "港股" (HK stocks)
  - "美股" (US stocks)
  - "沪深" (CN stocks)

Returns DataFrame with columns:
- `code`: Stock code
- `name`: Stock name
- `lot_size`: Lot size

#### get_all_watchlists()
Get all watchlist groups at once.

Returns dictionary mapping group names to DataFrames.

Example:
```python
client = FutuClient()
all_watchlists = client.get_all_watchlists()
for name, df in all_watchlists.items():
    print(f"{name}: {len(df)} stocks")
client.close()
```

## Trading Environment

- **TrdEnv.REAL**: Real trading (requires account and unlock)
- **TrdEnv.SIMULATE**: Paper trading (for testing)

## Error Handling

Always handle exceptions appropriately:

```python
from futu_client import FutuClient

client = FutuClient()

try:
    positions = client.get_positions()
except Exception as e:
    print(f"Error: {e}")

client.close()
```

## Notes

- FutuOpenD must be running before using this skill
- For real trading, you need to unlock with trading password
- Some features may require specific account permissions
- Paper trading (SIMULATE) is available for testing without real money
