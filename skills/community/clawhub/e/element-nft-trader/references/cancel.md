# Cancel

Use cancel to cancel existing orders created by the configured wallet.

## Required Before Execution

- `network` is confirmed
- the order object came directly from query results
- the order belongs to the configured wallet
- the order has the required cancel fields

## Do Not Proceed If

- the user only provided a transaction hash
- the user only provided a wallet address
- the user only provided an order ID but the full returned order object has not been recovered yet
- the available data is a summary instead of the full returned order object
- confirmation has not been received

Recommended flow:

1. Use `Query Account Orders` to find the user's active orders
2. If needed, use `Query Orders` with a `maker` filter to find matching orders
3. Cancel using the exact returned order object

## Cancellation Recovery Path

- If the user gives an `orderId`, first recover the full order object before canceling
- If the user gives a transaction hash, explain that it is not an order ID and use account or NFT context to find the related order
- If the user gives `contractAddress + tokenId`, query the relevant account orders and match the NFT before canceling
- If the user gives only a wallet address, first query that wallet's orders on the specified chain

## Cancel Parameters

- `network`: target network
- `operationType`: `cancel`
- `ordersToCancel`: array of order objects to cancel

Required fields from the order object:

| Field | Description | Example |
|-------|-------------|---------|
| `maker` | order creator address, must match the configured wallet | `"0x..."` |
| `schema` | token standard, `ERC721` or `ERC1155` | `"ERC721"` |
| `standard` | should be `element-ex-v3` | `"element-ex-v3"` |
| `exchangeData` | complete signed order payload | `'{"hash":"...",...}'` |

Fields often present but not required by cancel:

`orderId`, `side`, `contractAddress`, `tokenId`, `price`, `paymentToken`, `saleKind`, `listingTime`, `expirationTime`, `quantity`, `priceBase`, `priceUSD`, `taker`

Important notes:

- `exchangeData` contains the nonce and signed order details actually used on-chain
- `maker` must match the configured wallet
- `standard` must be `element-ex-v3`
- `schema` controls the cancel path
- Use the exact order object returned from query; do not modify fields
- Do not substitute a transaction hash, wallet address, or order summary for the required order object

System rules for cancel:

1. Show which orders will be canceled
2. Ask for explicit confirmation
3. Show transaction hash after submission
4. If needed, show the Element collection URL after resolving slug through `element-nft-tracker`

```bash
NETWORK="base"

ORDERS='[{"orderId":"...","maker":"0x...","contractAddress":"0x...","tokenId":"1","price":"10000000000000000",...}]'

INPUT=$(jq -n \
  --arg network "$NETWORK" \
  --argjson orders "$ORDERS" \
  '{
    confirmed: true,
    network: $network,
    operationType: "cancel",
    ordersToCancel: { orders: $orders }
  }')

node scripts/lib/entry.js "$INPUT"
```
