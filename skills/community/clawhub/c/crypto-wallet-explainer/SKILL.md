---
name: "crypto-wallet-explainer"
description: "AirnodeHub crypto skill to explain public wallet balances, history, NFTs, and live token prices via attested dRPC/CoinGecko POST reads; never request keys or transact."
---

# Crypto Wallet Explainer

## Execute

1. Extract the public address, chain scope, desired balances/history/NFT view, pricing currency, and detail. Treat the address and its association with the user as sensitive context: minimize repetition and do not persist or disclose it. Never request seed phrases, private keys, signing, wallet connection, or transaction approval; never transact. **Done when:** the task is strictly read-only.

2. Read current documentation at `https://airnode-drpc.fly.dev/` and `https://airnode-coingecko.fly.dev/`. Use only documented POST operations and parameters; GET only reads documentation. **Done when:** schemas, costs, signer addresses, and verification rules are known.

3. Use the narrowest dRPC operation: `walletBalances`, `chainWalletBalances`, `nonEvmWalletBalances`, `netWorthHistory`, `chainNetWorthHistory`, `transactionHistory`, `walletNfts`, `nonEvmWalletNfts`, `nftCollections`, or `nftMetadata`. Use `supportedChains` when chain resolution is necessary. Keep limits conservative and never silently paginate or broaden chain scope. **Done when:** the minimum wallet call is selected.

4. Use CoinGecko `simplePrice` for current prices with explicit CoinGecko IDs and currencies; use `coinsMarkets` only for richer ranked data. Resolve ambiguous symbols rather than guessing. **Done when:** only required pricing calls are selected.

5. Before any paid, credentialed, quota-consuming, or uncertain-cost POST, state the cost and scope and obtain explicit approval. POST `{"operation":"<operation>","parameters":{...}}` with an HTTP-capable tool. Retry once for corrected schema or transient failure. **Done when:** attested results or an exact blocker is received.

6. Explain results without implying ownership, identity, legality, intent, profit, tax basis, or investment quality. Separate facts from interpretation; flag spam tokens, unpriced assets, stale metadata, indexing gaps, pagination limits, unsupported chains, and valuation volatility. State currency and timestamp and shorten addresses unless exact display is needed. End with a brief read-only informational, not financial advice note. **Done when:** the answer is privacy-conscious and uncertainty is explicit.

## Verification

Confirm all data lookups used documented POST operations and the envelope contains `airnode`, `requestHash`, `timestamp`, `data`, and `signature`. Verify the documented request hash and EIP-191 signer when tooling is available; otherwise state that the signature was present but not cryptographically verified. Confirm wallet facts came from dRPC, prices from CoinGecko, timestamps and coverage limits were disclosed, and no secrets, signing, transactions, credentials, payment, or unapproved paid action occurred.
