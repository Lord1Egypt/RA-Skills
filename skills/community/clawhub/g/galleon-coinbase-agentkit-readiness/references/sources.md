# Official sources

Reviewed 2026-09-27. Recipes target CDP SDK v2 account APIs and the current AgentKit EVM provider interface. Record the installed exact versions at use time; no unpinned dependency is installed by this skill.

- [Coinbase AgentKit repository](https://github.com/coinbase/agentkit): framework integration and wallet/action provider separation; Node.js 22+ for current TypeScript quickstart.
- [EVM provider implementation](https://github.com/coinbase/agentkit/blob/main/typescript/agentkit/src/wallet-providers/cdpEvmWalletProvider.ts): environment names and initialization lifecycle. Inspect the installed revision before calling it.
- [CDP SDK](https://github.com/coinbase/cdp-sdk): installed types and existing-account retrieval.
- [API Key Wallet quickstart](https://docs.cdp.coinbase.com/wallet-api/v2/introduction/quickstart): separate creation, funding and transaction operations; none is a readiness test.
- [Agentic Wallet CLI](https://docs.cdp.coinbase.com/agentic-wallet/cli/quickstart): separate email authentication and read commands; current prerequisites specify Node.js 24+.
