# Python minimal mapping

目标：保留最小交易闭环，但扩展为可直接下单与管理订单。

## Python client shape

- class: `SimplePolymarketTrader`
- init args: `private_key`
- constants:
  - `CLOB_HOST = "https://clob.polymarket.com"`
  - `CHAIN_ID = 137`

## Auth flow (private.env + signing)

1. 从 `private.env` 读取 `POLYMARKET_PRIVATE_KEY`
2. `Account.from_key(private_key)` 初始化钱包对象
3. `ClobClient(host, chain_id, key=private_key)`
4. `derive_api_key()`，若无则 `create_api_key()`
5. 重新构造带 `creds` 的 `ClobClient(...)`

## Trading methods

下单前自动执行 allowance 检查/授权：
- BUY 前授权 `AssetType.COLLATERAL`
- SELL 前授权 `AssetType.CONDITIONAL`（对应 token）

- `market_buy(token_id, amount)` → `create_and_post_market_order(..., OrderType.FOK)`
- `market_sell(token_id, amount)` → `create_and_post_market_order(..., OrderType.FOK)`
- `limit_buy(token_id, price, size)` → `create_and_post_order(..., OrderType.GTC)`
- `limit_sell(token_id, price, size)` → `create_and_post_order(..., OrderType.GTC)`
- `get_open_orders()`
- `get_order(order_id)`
- `cancel_order(order_id)`
- `cancel_all()`

这份技能脚本对应上述最小实现。
