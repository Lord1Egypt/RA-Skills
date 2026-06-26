# Sell

Use sell for listing NFTs on Element Market.

## Required Before Execution

- `network` is confirmed
- NFT contract address is confirmed
- `tokenId` is confirmed
- listing price is confirmed
- `paymentToken` is resolved for the selected chain if the user wants a supported non-default currency

## Do Not Proceed If

- the NFT contract address is still ambiguous
- the user wants a non-default ERC20 price but the token is unsupported for that chain
- the user wants a stablecoin price but the payment token address has not been resolved
- the collection appears to be ERC1155 and quantity is still missing
- a custom ERC20 price is requested but `paymentToken` is being placed at the top level instead of inside the operation payload
- confirmation has not been received

## Minimum Success Path

1. Confirm `network`, collection address, `tokenId`, and price
2. If the user wants a custom currency, resolve `paymentToken` only when that chain-token pair is supported by [payment-tokens.md](references/payment-tokens.md)
3. If quantity is omitted, start with ERC721
4. If quantity is provided, or ERC721 fails due to schema, use ERC1155
5. Unless the user asked for a custom expiry, omit `expirationTime` so the SDK defaults to 7 days
6. Show preview and wait for confirmation

Price rule:

- For ERC1155 sell flows, the user-provided price is the total listing price by default, not the per-item unit price
- `erc1155sellOrder.paymentTokenAmount` represents the total order price for the full listed quantity
- Only treat the price as a unit price if the user explicitly says it is a per-item price
- In previews, always clearly distinguish `total price` from `unit price`
- For ERC1155 previews, show both values even when the user only provided one of them

## Sell Parameters

- `network`: target network
- `operationType`: `erc721sell` or `erc1155sell`
- `sellOrders.paymentToken`: optional for `erc721sell`; when omitted, the default payment currency for the target flow is used
- `erc1155sellOrder.paymentToken`: optional for `erc1155sell`; when omitted, the default payment currency for the target flow is used
- `sellOrders.items[].paymentTokenAmount` / `erc1155sellOrder.paymentTokenAmount`: base-unit amount. When using a supported custom token, convert with the token decimals from [payment-tokens.md](references/payment-tokens.md)
- `sellOrders.items` or `erc1155sellOrder`: payload described below

Important payload rules:

- For `erc721sell`, put `paymentToken` and `expirationTime` inside `sellOrders`
- For `erc1155sell`, put `paymentToken` and `expirationTime` inside `erc1155sellOrder`
- `expirationTime` is optional; if omitted, the SDK defaults it to 7 days from the current time
- Do not put `paymentToken` at the top level for sell flows; the sell executor will ignore it there
- If the requested ERC20 is not listed as supported for that chain, do not pass it as `paymentToken`
- If the requested ERC20 is supported for that chain, do not describe it as a collection restriction before a real execution error exists
- For ERC1155, `paymentTokenAmount` is the full order amount for the listed quantity unless the user explicitly asked for per-item pricing

Result handling rule:

- Use the returned `paymentToken` field to decide whether the completed order is native-token priced or ERC20-priced
- If the returned `paymentToken` is `0x0000000000000000000000000000000000000000`, do not describe the order as `USDT`, `USDC`, or any other ERC20
- For ERC1155 results, do not reinterpret the returned price as a platform-fee-adjusted unit price unless the API or chain data explicitly proves that; prefer describing it as the returned order price and keep the originally confirmed total price clear

## Minimal Payload Shapes

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "erc721sell",
  "sellOrders": {
    "paymentToken": "0x...",
    "expirationTime": 1775433600,
    "items": [
      {
        "erc721TokenAddress": "0x...",
        "erc721TokenId": "1",
        "paymentTokenAmount": "100000000"
      }
    ]
  }
}
```

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "erc1155sell",
  "erc1155sellOrder": {
    "assetAddress": "0x...",
    "assetId": "100001",
    "assetSchema": "ERC1155",
    "quantity": "3",
    "paymentToken": "0x...",
    "paymentTokenAmount": "100000000",
    "expirationTime": 1775433600
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.
