# Current Superfluid implementation tracks

Reviewed 2026-10-08. Resolve deployment, current ABI and rights at use time.

## Official SDK and metadata

[Official skills](https://github.com/superfluid-org/skills) provide protocol context, contract references and optional helpers. These installed Galleon procedures link them without bundling their scripts. [Current SDK guidance](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/sdks.md) selects `@sfpro/sdk` for viem/wagmi/ethers integrations; prior `sdk-core`, `sdk-redux` and `js-sdk` are deprecated for new projects.

[SDK documentation](https://sdk.superfluid.pro/docs) supplies ABI exports and chain-indexed addresses. For example, `cfaForwarderAbi`/`cfaForwarderAddress` come from `@sfpro/sdk/abi`; `hostAbi`/`hostAddress` from `@sfpro/sdk/abi/core`; schedulers from `@sfpro/sdk/abi/automation`. Resolve the chain key and verify onchain code. Do not handcraft an ABI from a remembered method signature.

Use the official `@superfluid-finance/metadata` for deployment/network resolution and tokenlist for token discovery, then corroborate token identity and underlying/wrapper conversion. Solidity build dependencies and client runtime dependencies have different roles.

## Agreement and real-time balance

[Architecture](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/architecture.md) distinguishes Host dispatch, CFA, GDA, Super Tokens and forwarders. A direct token transfer, wrapped balance, CFA flow and pool distribution are separate effects.

[Flowing balances](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/flowing-balances.md) explains time-dependent available balances. Capture observation time, current net rate, deposits and owed deposit using the actual contract return semantics. Rate × time predicts only under stated no-change assumptions; incoming flow changes, wrapping and liquidations alter it.

## Operators, schedulers and macros

[Official CFA reference](https://github.com/superfluid-org/skills/tree/main/skills/superfluid/references/contracts) contains current permission and rate-allowance interfaces. Check the actual ABI and current permission bits before preparing a delegation. Rate allowance is not an ERC20 token approval and does not automatically enforce a total lifetime spend.

[Macro clear-signing](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/clear-macro.md) and [forwarder guidance](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/guides/macro-forwarders.md) cover human-readable typed intent and execution. Preserve verified domain, target, nested operations and authorization; clear text does not replace exact call inspection.

[Flow scheduler](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/flow-scheduler-guide.md), [vesting scheduler](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/vesting-scheduler-guide.md) and [AutoWrap](https://github.com/superfluid-org/skills/blob/main/skills/superfluid/references/subgraphs/auto-wrap-guide.md) are additional modules. Inspect execution permissions, funding/allowance and actual schedule status. A configured automation is not an executed cancellation or guaranteed future funding.
