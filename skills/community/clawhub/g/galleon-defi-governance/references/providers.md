# Official governance providers

Sources accessed 2026-09-05. Documentation verified; no votes, alias authorizations, paid API calls or treasury actions were tested.

| Provider | Official interface | Access and scope |
|---|---|---|
| Snapshot | [Official MCP](https://docs.snapshot.box/tools/snapshot-mcp), `https://mcp.snapshot.box` | Public query/schema tools; writes use OAuth with a CDP-managed Snapshot alias. Configure a narrow read tool allowlist for research. Alias authorization creates delegated governance authority and is a separate user action. |
| Snapshot X | [Overview](https://docs.snapshot.box/snapshot-x/overview) and the official docs index | Onchain governance differs from classic offchain Snapshot. Follow the exact space/version's voting and execution model, including chain and execution strategy. |
| Cactus, formerly Tally | [Current docs](https://docs.tally.xyz/), [API](https://docs.tally.xyz/set-up-and-technical-documentation/welcome/how-to-use-the-tally-api/) | Official GraphQL API requires `Api-Key`; use documented schema, pagination and rate limits. The playground may expose unsupported fields. No official production MCP established here. |
| OpenZeppelin Governor | [Official lifecycle](https://docs.openzeppelin.com/contracts/5.x/governance) | Read deployed Governor/token/Timelock interfaces. Extensions determine counting, clock, roles, quorum and queue requirements. No universal ABI/clock assumptions across Governor variants. |
| Safe | [Official SDK](https://docs.safe.global/sdk/overview), [Protocol Kit](https://docs.safe.global/sdk/protocol-kit) | Owner signatures, Safe nonce, threshold, transaction service proposal and onchain execution are separate states. Inspect enabled modules/guards and actual executor. API access is not owner authority. |

## Snapshot tooling

The documented research tools are `snapshot-query` and `snapshot-schema`. Discover current schemas before use. `snapshot-whoami` is authenticated; vote/propose/follow tools mutate public state. A follow is an account action even though it moves no tokens. Do not enable all tools just because the server needs no key for reads.

An authorized alias can sign governance messages without the user's main key. Keep the alias token secret, record the exact scope and revocation path in Snapshot settings, and preserve user approval per action or explicitly bounded policy. Recalling the vote tool can replace an earlier vote; reconcile proposal+voter+choice before retrying after an ambiguous response.

## Governor and Cactus lifecycle

Use Cactus for discovery and human-readable proposals, then corroborate consequential state on the deployed contracts. A proposal's targets/values/calldata and description hash establish the action identity. Query the contract clock rather than estimating deadline from a universal block time. Snapshot voting power may require earlier delegation.

[Queue and execution](https://docs.tally.xyz/how-to-use-tally/proposals/managing-proposals/) depend on the DAO's Timelock and custom permissions. Passing does not mean executed. Re-read delay, readiness, cancellation state, needed native value and cross-chain messaging fees. A completed source execution can still await destination actions. Never infer authority from a permissionless contract method.
