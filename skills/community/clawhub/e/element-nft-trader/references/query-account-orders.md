# Query Account Orders

Use this when the user asks:

- "Show my orders"
- "What listings do I have?"
- "What has this wallet listed on Element?"

Ask for the required `network` first before executing this query. Do not iterate over multiple chains to find the user's orders.

This is account-specific and uses the unified `entry.ts` executor.

This queries orders for a specified account on a specified network.

If `wallet_address` is omitted, the query defaults to the account address associated with the configured API key. If `wallet_address` is provided, it can query another wallet's orders.

## Do Not Proceed If

- the payload uses `operation` instead of `operationType`
- `wallet_address`, `limit`, `cursor`, or `contract_address` are placed at the top level instead of inside `queryAccountOrders`
- `network` is missing

## Payload Rules

- Use top-level `operationType: "queryAccountOrders"`
- Use top-level `network: "base"` style network selection
- Put query-specific fields inside `queryAccountOrders`
- Do not flatten `wallet_address` or other query fields onto the top level

```json
{
  "operationType": "queryAccountOrders",
  "network": "base",
  "queryAccountOrders": {
    "wallet_address": "0x...",
    "limit": 20
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.

Returns:

- `chain`
- `usingDefaultAccount`
- `walletAddress`
- `count`
- normalized order summaries
- `orders[].expirationTime` as a readable UTC time string

Result display rules:

- If `count > 1`, do not describe the result as a single order
- When multiple orders are returned, list each order or explicitly say the output is truncated
- The displayed order count must match the actual returned `count`
