# API3 Data Feed Purchase

Helper skill for buying API3 data feed subscriptions from market.api3.org.

## Requirements

- `pnpm`
- `ts-node`
- `WALLET_MNEMONIC` in `.env` (see `example.env`)

## Scripts

- `get-dapis.ts` and `get-chains.ts` to discover supported feeds and networks
- `explore-data-feeds.ts` to inspect provider-reported values for a feed
- `quote.ts` to get a subscription price quote
- `buy.ts` to execute the purchase transaction
- `read-data-feed.ts` to read the deployed reader proxy
