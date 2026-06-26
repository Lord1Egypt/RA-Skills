# Get Wallet Address

Use this to derive the wallet address from the configured private key.

Parameters:

- `network`: target network
- `operationType`: `getAddress`

```bash
NETWORK="base"
INPUT=$(jq -n \
  --arg network "$NETWORK" \
  '{network: $network, operationType: "getAddress"}')
node scripts/lib/entry.js "$INPUT"
```

Expected response:

```json
{
  "status": "success",
  "operation": "getAddress",
  "address": "0x..."
}
```
