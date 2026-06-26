# Bitpanda API Reference

Base URL: `https://developer.bitpanda.com`
Auth: `X-Api-Key: <API_KEY>` header on every request.

Pagination: cursor-based via `before`, `after`, and `page_size` (max 100, default 25).
All endpoints cover all asset types (crypto, fiat, stocks, ETFs, metals, indices).

### GET /v1/wallets/
List all user wallets (balances) across all asset types.

| Param | Type | Description |
|---|---|---|
| asset_id | string (uuid) | Filter by asset ID |
| index_asset_id | string (uuid) | Filter by index asset ID |
| last_credited_at_from_including | string (datetime) | Filter wallets credited at >= date |
| last_credited_at_to_excluding | string (datetime) | Filter wallets credited at < date |
| before | string | Return page before cursor |
| after | string | Return page after cursor |
| page_size | int | Items per page (1-100, default 25) |

Response shape:
```json
{
  "start_cursor": "string",
  "end_cursor": "string",
  "has_previous_page": false,
  "has_next_page": true,
  "page_size": 25,
  "data": [
    {
      "wallet_id": "uuid",
      "asset_id": "uuid",
      "wallet_type": "STAKING | CRYPTO_INDEX | null",
      "index_asset_id": "uuid | null",
      "last_credited_at": "2024-01-15T10:30:00Z",
      "balance": 1.23456789
    }
  ]
}
```

To resolve `asset_id` to a human-readable name/symbol, use `GET /v1/assets/{asset_id}`.

### GET /v1/transactions
List all user transactions across all asset types. Newest first. Cursor paginated.

| Param | Type | Description |
|---|---|---|
| wallet_id | string (uuid) | Filter by wallet ID |
| flow | string | `incoming` or `outgoing` |
| asset_id | string (uuid) | Filter by asset ID (repeatable) |
| from_including | string (datetime) | Transactions credited at >= date |
| to_excluding | string (datetime) | Transactions credited at < date |
| before | string | Return page before cursor |
| after | string | Return page after cursor |
| page_size | int | Items per page (1-100, default 25) |

Response shape:
```json
{
  "start_cursor": "string",
  "end_cursor": "string",
  "has_previous_page": false,
  "has_next_page": true,
  "page_size": 25,
  "data": [
    {
      "transaction_id": "uuid",
      "operation_id": "uuid",
      "asset_id": "uuid",
      "account_id": "uuid",
      "wallet_id": "uuid",
      "asset_amount": 0.5,
      "fee_amount": 0.001,
      "operation_type": "string",
      "transaction_type": "string | null",
      "flow": "incoming | outgoing",
      "credited_at": "2024-01-15T10:30:00Z",
      "compensates": "uuid | null",
      "trade_id": "uuid | null"
    }
  ]
}
```

### GET /v1/assets/{asset_id}
Get asset information by asset ID.

Response shape:
```json
{
  "data": {
    "id": "uuid",
    "name": "Bitcoin",
    "symbol": "BTC"
  }
}
```

### GET /v1/ticker
Returns current prices for all available assets. Cursor-paginated.

| Param | Type | Description |
|---|---|---|
| page_size | int | Items per page (max 500) |
| cursor | string | Cursor for next page |

Response shape:
```json
{
  "data": [
    {
      "id": "uuid",
      "symbol": "BTC",
      "type": "cryptocoin",
      "currency": "EUR",
      "price": "95000.00000000",
      "price_change_day": "1.33"
    }
  ],
  "next_cursor": "string",
  "has_next_page": true
}
```
