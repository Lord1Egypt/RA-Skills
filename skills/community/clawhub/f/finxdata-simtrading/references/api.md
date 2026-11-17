# FinXData A 股/港股模拟交易 API

当前状态：A 股和港股模拟账户、下单、持仓、成交、资金、资产与收益接口均已开放。

Base prefix: `/api/sim-trading/v1`

Authentication: `X-FINXDATA-TRADING-KEY: <trading_key>`. The dedicated key grants access to every simulated-trading operation. `X-API-Key` is not accepted, and Agent callers do not need a login JWT.

Usage behavior: each successful key authentication increments that key's `call_count` and updates `last_used_at`. Calls do not deduct or write `api_call_log` usage for trial/basic/premium data quota. Mutating calls use the separate per-user simulated-trading write limiter (default 30/minute).

Market scope: watchlist and simulated trading accept known A-share and Hong Kong stock codes from the security master. Accounts are market-isolated: `CN` accounts use CNY and T+1, while `HK` accounts use HKD and T+0. Cross-market orders return `ACCOUNT_MARKET_MISMATCH`.

## Watchlist

| Method | Path | Client method | Purpose |
| --- | --- | --- | --- |
| GET | `/watchlist` | `list_watchlist()` | List the current user's watchlist with latest stored daily price |
| POST | `/watchlist` | `add_watchlist(stock_code, note=None, sort_order=0)` | Add a known security; duplicate code returns `WATCHLIST_ITEM_EXISTS` |
| DELETE | `/watchlist/{stock_code}` | `remove_watchlist(stock_code)` | Remove one current-user item |

POST body:

```json
{"stock_code":"600519","note":"长期观察","sort_order":0}
```

List response fields include `stock_code`, `stock_name`, `market`, `exchange`, `board`, `note`, `sort_order`, `latest_price`, `change_pct`, and `price_date`. The server limits each user to `max_items` (default 100).

## Accounts and Trading

| Method | Path | Client method |
| --- | --- | --- |
| GET / POST | `/accounts` | `list_accounts(status="active", market=None, cursor=None, limit=50)` / `create_account(..., market="CN")` |
| GET | `/accounts/{account_id}` | `get_account(account_id)` |
| POST | `/accounts/{account_id}/reset` | `reset_account(account_id, confirmation="RESET")` |
| GET / POST | `/accounts/{account_id}/orders` | `list_orders(...)` / `place_order(...)` |
| GET | `/accounts/{account_id}/orders/{order_id}` | `get_order(...)` |
| POST | `/accounts/{account_id}/orders/{order_id}/cancel` | `cancel_order(...)` |
| GET | `/accounts/{account_id}/positions` | `list_positions(account_id)` |
| GET | `/accounts/{account_id}/positions/{stock_code}` | `get_position(...)` |
| GET | `/accounts/{account_id}/trades` | `list_trades(...)` |
| GET | `/accounts/{account_id}/cash-ledgers` | `list_cash_ledgers(...)` |
| GET | `/accounts/{account_id}/assets` | `get_assets(account_id)` |
| GET | `/accounts/{account_id}/performance` | `get_performance(...)` |

Account listing defaults to active accounts and returns `next_cursor`; pass `market=CN|HK` to filter or `status=archived`, `disabled`, or `all` to inspect history.

Create an A-share account with `{"name":"A股账户","market":"CN","initial_cash":"100000"}` or a Hong Kong account with `{"name":"港股账户","market":"HK","initial_cash":"100000"}`. Omit `settlement_mode` to receive the market default. Account, position, and asset responses include `currency` (`CNY` or `HKD`).

Orders require an explicit unique `client_order_id` per account. Create it before the first request and preserve it across timeouts or connection retries. Reusing it with identical parameters is idempotent; reusing it with different parameters returns a conflict. Market orders omit `limit_price`; limit orders require it.

Hong Kong order codes may be written as `00700`, `HK00700`, or `00700.HK`. In relaxed mode, a Hong Kong buy must start at the security's `lot_size`; quantities above that threshold and all sells increment by one share. Do not assume a universal lot size. Hong Kong buys are immediately available to sell under T+0.

Orders can execute at any time. During a confirmed live A-share or Hong Kong session, the latest quote must be from the current trading day and within the configured freshness threshold. Before market open, during the midday break, after market close, and on non-trading days, execution uses the latest trusted persisted quote; inspect `quote_time` in the response to understand the snapshot used.

Hong Kong fees use rule `HK_STOCK_SIM_FEE/1.0`: simulated commission plus stock stamp duty, SFC levy, AFRC levy, HKEX trading fee, and settlement fee. For response compatibility, the four regulatory/exchange/settlement charges are aggregated into `transfer_fee`. Historical fills preserve the calculated fee fields and rule version.

Order create, detail, and list responses include `quote_price` and `quote_time` so an Agent can audit the persisted market snapshot used for execution.

## Common Errors

| Code | Meaning |
| --- | --- |
| `SIM_TRADING_AUTH_REQUIRED` | Neither the dedicated trading key nor browser JWT was provided |
| `INVALID_TRADING_KEY` | Trading key is malformed, unknown, revoked, or belongs to a disabled user |
| `STOCK_NOT_FOUND` | Code is absent from local security master data |
| `WATCHLIST_ITEM_EXISTS` | User already follows the code |
| `WATCHLIST_ITEM_NOT_FOUND` | User does not follow the code |
| `WATCHLIST_LIMIT_EXCEEDED` | Per-user watchlist capacity reached |
| `SIM_ACCOUNT_NOT_FOUND` | Account is absent, archived where active is required, or belongs to another user |
| `ACCOUNT_MARKET_MISMATCH` | The security and simulated account belong to different markets |
| `MARKET_NOT_SUPPORTED` | The security metadata does not map to an enabled CN or HK rule |
| `INVALID_ORDER_QUANTITY` | Quantity is below the board minimum or otherwise invalid |
| `QUOTE_UNAVAILABLE` / `QUOTE_STALE` | A trusted persisted quote is unavailable, or the quote is stale during a live session |
| `INSUFFICIENT_CASH` / `INSUFFICIENT_POSITION` | Simulated funds or holdings are insufficient |
| `IDEMPOTENCY_CONFLICT` | Client order ID was reused with different order parameters |
| `SIM_TRADING_RATE_LIMITED` | Independent write limit exceeded |

Business errors use `{"code":"...","message":"...","trace_id":"...","details":{...}}`.
