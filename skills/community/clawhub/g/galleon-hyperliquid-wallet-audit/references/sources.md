# Sources verified 2026-10-09

- [Official Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint): account identity, open-order/fill schemas, time-range pagination, 2000-fill response bound, 10000-fill retention, role and account abstraction.
- [Official perpetual Info endpoints](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals): default DEX account/position state, funding ledger schema and signed `usdc` values, unified/portfolio-margin balance caveat.
- [Official spot Info endpoints](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot): token balances and unified/portfolio-margin balance source.
- [Official SDK network constants](https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/master/hyperliquid/utils/constants.py): mainnet/testnet API URLs.

The helper and accounting code are independently authored. It contains no competitor SDK, copied signer or provider dependency. Public-wallet analytics research motivates a reproducible diagnostic, with unsupported ranking and portfolio claims deliberately excluded from the output.
