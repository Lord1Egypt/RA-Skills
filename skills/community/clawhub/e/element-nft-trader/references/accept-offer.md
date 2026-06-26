# Accept Offer

Use this when the user wants to sell into an existing buy order or collection offer.

## Required Before Execution

- `network` is confirmed
- the selected order object came directly from `query`
- the selected order is a buy-side order
- `assetId` is confirmed for collection-wide offers
- ERC1155 quantity is confirmed when needed

## Do Not Proceed If

- the selected order is only a summary and not the full returned order object
- a collection-wide offer is selected but `assetId` is still missing
- an ERC1155 quantity is missing
- confirmation has not been received

## Order Selection Rules

Only choose orders that satisfy all of these:

- `side=0` because `acceptOffer` fills buy-side orders
- The order object came directly from `query` output; do not manually rebuild it
- If `saleKind=7`, treat it as a collection-wide offer even if the returned `tokenId` is `0`
- If the offer is collection-wide, collect `assetId` before execution
- If the offer targets ERC1155, confirm the requested quantity before execution
- Do not execute against a generic order summary that is missing the original order fields

## Minimum Success Path

1. Query buy-side orders with `side=0`
2. Let the user choose one exact returned order object
3. Ask for `assetId` if the offer is collection-wide
4. Ask for `quantity` if the offer is ERC1155
5. Show preview and wait for confirmation

## Accept Offer Parameters

- `network`: target network
- `operationType`: `acceptOffer`
- `acceptOfferOrder.order`: required order object returned by query
- `acceptOfferOrder.assetId`: optional token ID, but required for collection-wide offers
- `acceptOfferOrder.quantity`: optional, default `1`

Important notes:

- Use buy-side orders only: `side=0`
- For collection-wide offers (`saleKind=7`), `assetId` is required when accepting the offer
- Do not display a collection-wide offer as token `#0`; `tokenId=0` in this case is not a real NFT selection
- For ERC1155 offers, `quantity` must not exceed the offered fillable amount
- The SDK may set NFT approval before executing the final trade transaction
- Unlike ERC20-priced `buy`, `acceptOffer` does not need `paymentTokenDecimals` because it fills a buy-side order and approves the NFT side instead of calculating ERC20 approval

## Minimal Payload Shape

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "acceptOffer",
  "acceptOfferOrder": {
    "order": {
      "orderId": "...",
      "contractAddress": "0x...",
      "schema": "ERC721",
      "standard": "element-ex-v3",
      "maker": "0x...",
      "paymentToken": "0x...",
      "price": "0.003",
      "saleKind": 7,
      "side": 0
    },
    "assetId": "22",
    "quantity": "1"
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.
