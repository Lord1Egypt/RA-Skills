# Buy

Buy fills sell-side orders returned by `query`.

## Required Before Execution

- `network` is confirmed
- the selected order objects came directly from `query`
- the chosen orders are sell-side orders
- ERC1155 quantities are confirmed when needed

## Do Not Proceed If

- the selected orders are only summarized manually instead of using the full returned objects
- an ERC1155 quantity is missing or exceeds available quantity
- the selected orders and quantities arrays are misaligned
- confirmation has not been received
- validation failed because required order fields were missing

## Order Selection Rules

Only choose orders that satisfy all of these:

- `side=1` because `buy` fills sell-side orders
- The order object came directly from `query` output; do not manually rebuild it
- The object still contains the original query-returned fields needed for execution, rather than a hand-written subset
- For ERC1155, confirm the requested quantity does not exceed the available quantity
- For multi-order buys, keep `buyOrders.orders` and `buyOrders.quantities` aligned by index
- Do not mix unrelated orders just because they share the same collection
- If the order is priced in an ERC20 token such as `USDT` or `USDC`, buy one order at a time

## Minimum Success Path

1. Query sell-side orders with `side=1`
2. Let the user choose exact returned order objects
3. Ask for `quantity` on ERC1155 orders
4. If the order uses an ERC20 payment token, execute it as a single-order buy so the SDK can handle approval
5. Show selected orders, quantities, and total cost
6. Wait for confirmation

If validation reports missing order fields, stop and go back to `query`. Do not manually add fields such as `side`, `standard`, or `maker` just to satisfy validation.

## Buy Parameters

- `network`: target network
- `operationType`: `buy`
- `buyOrders.orders`: array of order objects
- `buyOrders.quantities`: required for ERC1155, must align with `orders`
- `buyOrders.orders[].paymentTokenDecimals`: required for ERC20-priced orders; get it from [payment-tokens.md](references/payment-tokens.md)

What the SDK actually uses:

The SDK sends `orderId` + `takeCount` to the API, which returns the blockchain call data (`to`, `value`, `data`). Other order fields are mainly used to support the user-facing workflow: previewing the purchase, selecting orders, showing quantity and cost, and preparing follow-up actions such as cancellation.

Important notes:

- For ERC721, quantities can be omitted and default to `1`
- For ERC1155, quantities are required and must not exceed available quantity
- The quantities array must match the orders array length
- For partial ERC1155 fills, actual cost is `order.price * (purchaseQuantity / order.quantity)`
- Native-token priced orders use the batch buy path
- ERC20-priced orders such as `USDT` or `USDC` use a single-order fill path
- Do not batch multiple ERC20-priced orders together
- For ERC20-priced orders, always pass `paymentTokenDecimals` instead of relying on runtime detection

## Failure Triage

- If buy validation fails because order fields are missing, re-run `query` and use the exact returned order object
- If buy fails with `UNPREDICTABLE_GAS_LIMIT`, first suspect stale order state, incomplete order data, or invalid quantity; do not immediately blame wallet gas balance
- If buy validation reports missing `paymentTokenDecimals`, look it up from the payment token reference and retry; do not guess
- Do not infer insufficient `BNB` or token balance unless you have explicit balance evidence or an error that clearly points to insufficient funds

## Minimal Payload Shapes

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "buy",
  "buyOrders": {
    "orders": [
      {
        "orderId": "...",
        "contractAddress": "0x...",
        "tokenId": "1",
        "schema": "ERC721",
        "standard": "element-ex-v3",
        "maker": "0x...",
        "price": "0.1",
        "paymentToken": "0x...",
        "paymentTokenDecimals": 18,
        "side": 1
      }
    ]
  }
}
```

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "buy",
  "buyOrders": {
    "orders": [
      {
        "orderId": "...",
        "contractAddress": "0x...",
        "tokenId": "1",
        "schema": "ERC1155",
        "standard": "element-ex-v3",
        "maker": "0x...",
        "price": "0.0001",
        "paymentToken": "0x...",
        "paymentTokenDecimals": 6,
        "side": 1,
        "quantity": "5"
      }
    ],
    "quantities": ["3"]
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.
