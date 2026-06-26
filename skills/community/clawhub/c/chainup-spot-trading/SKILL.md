---
name: chainup-spot
description: ChainUp/OpenAPI V2 spot and margin trading skill. Prefer using the Python script to call `sapi` endpoints through one unified entrypoint and avoid ad hoc signing logic.
---

# ChainUp Spot (Script-First)

## Why This Skill

Use this skill immediately when the user mentions OpenAPI V2, spot trading, margin trading, `X-CH-SIGN`, `/sapi/v2/order`, `/sapi/v1/margin/*`, `/sapi/v1/account`, or similar ChainUp trading/account scenarios.

Goals:
- Prefer the script entrypoint instead of rebuilding signing logic each time.
- Return raw exchange JSON by default.
- If some parameters are still unknown, keep placeholders (`TODO`) first and let the user fill them in later.
- After the skill triggers, move to the script call quickly and avoid unnecessary explanation, extra reasoning, or repeated confirmation.

## Runtime Entry

Unified entry script:
- `scripts/chainup_api.py`

Core capabilities:
- Built-in signing: `X-CH-APIKEY`, `X-CH-SIGN`, `X-CH-TS`
- Built-in common headers: `Content-Type`, `admin-language`, `User-Agent`
- Unified `action -> endpoint` mapping
- Real balance-changing actions require `--confirm CONFIRM` by default
- Order actions support `--prepare-only`: fetch symbol rules via `spot_symbols` first, then preprocess `price` / `volume`
- Supports `--show-todo` to display unresolved required placeholders for the current action

## Execution Rules

- When this skill is triggered, call `scripts/chainup_api.py` first. Do not restate API parameter planning in natural language before using the script.
- For read-only actions that do not affect balances or order state, call the script directly once parameters are clear. Only ask follow-up questions when required parameters are missing and cannot be inferred safely.
- For any action that can change balances, positions, open orders, or fills, provide a short execution summary in natural language before the live request, then wait for the user to reply with an exact standalone `Confirm` before calling the script.
- For non-fund-changing queries, avoid extra confirmation and execute directly.
- Do not treat "the user wants to place/cancel/transfer" as execution permission. No live request is allowed until a separate user message contains `Confirm`.
- For `spot_create_order`, `spot_test_order`, and `margin_create_order`, run the script with `--prepare-only` before asking for confirmation. The script will call `spot_symbols`, fetch symbol precision, and round down using `pricePrecision` / `quantityPrecision`.
- When showing parameters that need confirmation, always use the `preparedBody` from `--prepare-only`. Do not show the unadjusted raw order payload.
- After the user sends a standalone `Confirm`, execute the live balance-changing action and keep using `--confirm CONFIRM`.
- If `spot_create_order` succeeds, follow up with `spot_get_order` by default.
- All HTTP requests must be sent through `scripts/chainup_api.py`.
- If the script call fails, return the script failure result and continue debugging through the Python script only. Do not switch to `curl`, handwritten signing, or any backup HTTP implementation.
- Do not add a second implementation "just to verify the API". Avoid branching logic and duplicated reasoning.

## Required Config

Prefer `/root/TOOLS.md` first:
- `BASE_URL: ...`
- `API_KEY: ...`
- `SECRET_KEY: ...`

Use environment variables only as the next fallback:
- `CHAINUP_BASE_URL`
- `CHAINUP_API_KEY`
- `CHAINUP_SECRET_KEY`

CLI arguments are also supported:
- `--base-url`
- `--api-key`
- `--secret-key`

Config resolution priority:
- `CLI arguments` > `/root/TOOLS.md` > `environment variables`
- If `/root/TOOLS.md` already contains usable credentials, use them directly and do not require the user to set environment variables first.

Sensitive data handling:
- `CHAINUP_API_KEY` and `CHAINUP_SECRET_KEY` are sensitive. Never print them in full in the terminal, natural-language responses, execution summaries, error relays, or example commands.
- If they must be referenced, only show masked values: keep the first 4 and last 4 characters and replace the middle with `***`, for example `915c***815e`.
- Avoid inlining secrets in visible commands whenever possible. If a command must include them, do not repeat that full secret-bearing command in the response.
- Even if the user provides the full secret explicitly, never echo it back verbatim later.

## Call Template

```bash
python /root/.codex/skills/chainup-spot/scripts/chainup_api.py <action> \
  --query-json '<json-object>' \
  --body-json '<json-object>' \
  --show-todo
```

Notes:
- Use `--query-json` for `GET` actions
- Use `--body-json` for `POST` actions
- For order actions, `--prepare-only` can be used first to return precision-adjusted `preparedBody` for confirmation
- For actions that change balances or orders, append `--confirm CONFIRM` only after the user sends a standalone `Confirm`
- Unless the user asks for explanation, prefer executing first and returning the result instead of giving a long preface

## Action Map

Public:
- `spot_ping` -> `GET /sapi/v2/ping`
- `spot_time` -> `GET /sapi/v2/time`
- `spot_symbols` -> `GET /sapi/v2/symbols`
- `spot_depth` -> `GET /sapi/v2/depth`
- `spot_ticker` -> `GET /sapi/v2/ticker`
- `spot_trades` -> `GET /sapi/v2/trades`
- `spot_klines` -> `GET /sapi/v2/klines`

Spot Signed:
- `spot_create_order` -> `POST /sapi/v2/order`
- `spot_test_order` -> `POST /sapi/v2/order/test`
- `spot_batch_orders` -> `POST /sapi/v2/batchOrders`
- `spot_get_order` -> `GET /sapi/v2/order`
- `spot_cancel_order` -> `POST /sapi/v2/cancel`
- `spot_batch_cancel` -> `POST /sapi/v2/batchCancel`
- `spot_open_orders` -> `GET /sapi/v2/openOrders`
- `spot_my_trades` -> `GET /sapi/v2/myTrades`

Account Signed:
- `spot_account` -> `GET /sapi/v1/account`
- `asset_transfer` -> `POST /sapi/v1/asset/transfer`
- `asset_transfer_query` -> `POST /sapi/v1/asset/transferQuery`

Margin Signed:
- `margin_create_order` -> `POST /sapi/v1/margin/order`
- `margin_get_order` -> `GET /sapi/v1/margin/order`
- `margin_cancel_order` -> `POST /sapi/v1/margin/cancel`
- `margin_open_orders` -> `GET /sapi/v1/margin/openOrders`
- `margin_my_trades` -> `GET /sapi/v1/margin/myTrades`

## Response Rules

- Return raw JSON by default (script stdout).
- `--prepare-only` returns `originalBody`, `preparedBody`, `adjustments`, and `symbolRule` so the user can review the precision-adjusted live order payload before confirmation.
- After a successful `spot_create_order`, immediately follow with `spot_get_order` by default and return the latest order details.
- When fetching the follow-up order, prefer `symbol + orderId` from the create-order response. If the gateway also returns `orderIdString`, preserve it as well.
- `spot_account` is filtered directly in the Python script and returns only assets where `free > 0` or `locked > 0`.
- Add a short summary only when the user asks to "show just the key points".
- If returned content, errors, or debug output contains full `api-key`, `secret-key`, or other credentials, mask them before showing anything.

## Safety Rules

- All live balance-changing actions (place order, cancel order, transfer) require the user to send `Confirm` manually before execution, then use `--confirm CONFIRM`.
- Any action that affects balances, even if it may not fill immediately, is still treated as a live balance-changing action. This includes but is not limited to limit orders, batch orders, cancellations, transfers, margin orders, and margin cancellations.
- Query actions can execute directly, including but not limited to balance queries, order queries, trade history queries, market data queries, and open-order queries.
- Precision prechecks are mandatory before order confirmation so the script does not send prices or quantities that exceed symbol precision to the live gateway.
- If the user explicitly requests to bypass confirmation, `--no-confirm-gate` may be used. This is high risk and should only be used with explicit user authorization.
- Never print full credentials in the terminal or reply. If the script throws an error that could expose secrets, summarize the failure rather than copying the raw sensitive output.

## Examples

Query spot balances:
```bash
python /root/.codex/skills/chainup-spot/scripts/chainup_api.py spot_account --query-json '{}'
```

Spot market order preparation (live request requires confirmation):
```bash
python /root/.codex/skills/chainup-spot/scripts/chainup_api.py spot_create_order \
  --body-json '{"symbol":"BTC/USDT","volume":"100.123456","side":"BUY","type":"MARKET"}' \
  --prepare-only
```

Execute the live request after confirmation:
```bash
python /root/.codex/skills/chainup-spot/scripts/chainup_api.py spot_create_order \
  --body-json '{"symbol":"BTC/USDT","volume":"100","side":"BUY","type":"MARKET"}' \
  --confirm CONFIRM --show-todo
```

Additional spot order conventions:
- When `type=MARKET` and `side=BUY`, `volume` is interpreted in the quote asset.
- For example, for `ETH/USDT`, `volume=1` with `side=BUY` means buying ETH with `1 USDT` at market.
- When `type=MARKET` and `side=SELL`, `volume` is interpreted in the base asset amount.
- For example, for `ETH/USDT`, `volume=0.1` with `side=SELL` means selling `0.1 ETH` at market.
- For non-market order types such as `LIMIT`, `volume` is still interpreted as the base asset amount.
- After `spot_create_order` succeeds, the default next step is not just returning the order receipt. The script should continue with `spot_get_order` and return the latest order information.

Margin limit order:
```bash
python /root/.codex/skills/chainup-spot/scripts/chainup_api.py margin_create_order \
  --body-json '{"symbol":"BTC/USDT","volume":"0.001","side":"BUY","type":"LIMIT","price":"30000"}' \
  --confirm CONFIRM --show-todo
```

## References

- Authentication and signing: [`references/authentication.md`](./references/authentication.md)
- Spot endpoints: [`references/spot-endpoints.md`](./references/spot-endpoints.md)
- Margin endpoints: [`references/margin-endpoints.md`](./references/margin-endpoints.md)
