# Check Wallet Balances

## Steps

1. Call `get_balances` to retrieve all assets.
2. Convert the ADA amount from lovelace: `amount / 1_000_000`.
3. Present ADA balance first, then list native assets with their names and amounts.

## Example prompt

> "What's in my wallet?"

## Example response

- **ADA:** 1,250.45 ADA
- **INDY:** 500 tokens
- **HOSKY:** 1,000,000 tokens
