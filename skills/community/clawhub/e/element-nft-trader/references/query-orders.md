# Query Orders

Use this to query public orders for a collection. This is collection-based discovery, not account-based order lookup.

Use cases:

- Browse current listings for a collection
- Find orders before buying
- Filter a collection's orders by token ID, price sort, or maker

Ask for the required `network` and collection address before executing this query. Do not query every chain to search for the collection.

If the user gives only a single `0x...` value, first ask for the `network`, then confirm whether that value is the collection contract address. Do not immediately describe it as an Element order hash, and do not ask for `token ID` unless the user wants to narrow the query.

## Minimum Success Path

1. Confirm `network` and collection address
2. Add optional filters only if the user actually asked for them
3. Use `side=1` for listings and `side=0` for offers
4. Return the full structured query result so later `buy`, `acceptOffer`, or `cancel` can reuse the exact order object
5. When showing offers, interpret `sale_kind` before describing the token target

## Query Parameters

- `network`: target network
- `operationType`: `query`
- `queryOrders.asset_contract_address`: required collection address
- `queryOrders.token_ids`: optional, token ID array
- `queryOrders.sale_kind`: optional order type filter. Use `0` for standard orders, `3` for bulk listings, `7` for collection offers. If omitted, do not filter by sale kind
- `queryOrders.side`: optional, `1=sell`, `0=buy`
- `queryOrders.maker`: optional maker address filter
- `queryOrders.payment_token`: optional payment token contract address filter. If omitted, do not filter by payment token
- `queryOrders.order_by`: optional, `created_date` or `base_price`
- `queryOrders.direction`: optional, `asc` or `desc`
- `queryOrders.listed_before`: optional Unix timestamp in seconds. If set, only return orders listed before this time. No default filter
- `queryOrders.listed_after`: optional Unix timestamp in seconds. If set, only return orders listed after this time. No default filter
- `queryOrders.limit`: optional, max 50, default 20
- `queryOrders.offset`: optional, default 0

```json
{
  "network": "base",
  "operationType": "query",
  "queryOrders": {
    "asset_contract_address": "0x...",
    "token_ids": ["1", "2"],
    "side": 1,
    "maker": "0x...",
    "payment_token": "0x...",
    "order_by": "base_price",
    "direction": "asc",
    "listed_before": 1775433600,
    "listed_after": 1774828800,
    "limit": 20,
    "offset": 0
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.

## Display Rules For Offers

- If `side=0` and `sale_kind=7`, this is a collection-wide offer
- Do not describe a `sale_kind=7` order as token `#0` even if the returned `tokenId` is `0`
- For collection-wide offers, present it as a collection offer and ask for the real `assetId` only when the user wants to accept it
- Resolve the payment token label by exact `chain + paymentToken address` match from [payment-tokens.md](references/payment-tokens.md)
- Do not guess `USDT`, `USDC`, `BUSD`, or any other symbol from decimals or chain defaults
- Do not present an unsupported ERC20 as if this skill supports it on that chain
- If the payment token address is not recognized, display the price as `[PRICE] [PAYMENT_TOKEN_ADDRESS]` or `[PRICE] unknown ERC20`
