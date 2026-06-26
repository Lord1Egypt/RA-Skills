# Offer

Use offer to create a buy order.

## Required Before Execution

- `network` is confirmed
- NFT contract address is confirmed
- `assetSchema` is explicitly confirmed as `ERC721` or `ERC1155`
- offer price is confirmed
- `paymentToken` is resolved if the user wants a supported specific ERC20 token

## Do Not Proceed If

- the payment token is still ambiguous
- the requested ERC20 is unsupported for that chain
- `assetSchema` is still implicit or guessed
- the user wants to use a native token instead of an ERC20 payment token
- the offer is token-specific and `assetId` is still missing
- the offer targets ERC1155 and `quantity` is still missing
- confirmation has not been received

## Minimum Success Path

1. Confirm `network`, collection address, `assetSchema`, and offer price
2. Resolve `paymentToken` only if the user wants a supported specific ERC20 token from [payment-tokens.md](references/payment-tokens.md)
3. Leave `assetId` empty for collection-wide offers
4. Add `assetId` for token-specific offers
5. Add `assetSchema` and `quantity` for ERC1155
6. Show preview and wait for confirmation

## Offer Parameters

- `network`: target network
- `operationType`: `offer`
- `offerOrder.assetAddress`: required NFT contract address
- `offerOrder.paymentTokenAmount`: required base-unit amount. Convert it using the token decimals from [payment-tokens.md](references/payment-tokens.md)
- `offerOrder.paymentToken`: optional ERC20 payment token address; native tokens are not supported for offers. When omitted, the offer typically uses the chain's wrapped native ERC20 token such as WETH or WBNB
- `offerOrder.expirationTime`: optional expiration timestamp
- `offerOrder.assetId`: optional token ID
- `offerOrder.assetSchema`: required, `ERC721` or `ERC1155`
- `offerOrder.quantity`: optional, default `1`

Notes:

- For collection-wide offers, do not specify `assetId`
- For specific-token offers, specify `assetId`
- Always explicitly set `assetSchema`; do not assume `ERC721`
- For ERC1155 offers, set `assetSchema` and `quantity`
- Offer payment tokens must be ERC20 tokens; do not use the native token address for offer creation
- If the requested ERC20 is not listed as supported for that chain, do not use it for offer creation

## Minimal Payload Shapes

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "offer",
  "offerOrder": {
    "assetAddress": "0x...",
    "assetSchema": "ERC721",
    "paymentTokenAmount": "100000000",
    "paymentToken": "0x...",
    "expirationTime": 1775433600
  }
}
```

```json
{
  "network": "base",
  "confirmed": true,
  "operationType": "offer",
  "offerOrder": {
    "assetAddress": "0x...",
    "assetId": "100001",
    "assetSchema": "ERC1155",
    "quantity": "2",
    "paymentTokenAmount": "100000000",
    "expirationTime": 1775433600
  }
}
```

Run with `node scripts/lib/entry.js "$INPUT"`.
