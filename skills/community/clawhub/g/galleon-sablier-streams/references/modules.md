# Sablier modules and official interfaces

Reviewed 2026-10-08; resolve current ABI and deployment at use time.

## Official procedure source

[Sablier agent skills](https://github.com/sablier-labs/sablier-skills) provide separate create, withdraw and cancel recipes for Flow, Lockup and airdrops. Reuse the selected maintained source after reviewing its version and signing behavior; no upstream runtime is bundled here. Never run a broadcast example as discovery. A bulk default is not authority to act on every stream.

[Flow creation integration](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-create-open-ended-stream/references/evm-onchain.md) documents `create` and `createAndDeposit`. Creation returns a stream ID and mints an ERC-721 to recipient. `ratePerSecond` uses UD21x18, encoded with 18 decimals independent of ERC20 decimals. Funding uses token base units. `startTime=0` selects block time; past starts accrue retroactively. The current deployment/ABI governs exact parameters.

## Flow debt and cancellation

[Flow overview](https://docs.sablier.com/concepts/flow/overview) explains continuously accruing debt and flexible funding. Read covered/uncovered debt and withdrawable amounts. Pausing stops future accrual while retaining accrued obligations. Voiding is permanent and can forfeit uncovered debt. Exact caller permissions need current sender/recipient rights.

[Official cancellation recipe](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-cancel-open-ended-stream/references/cli.md) uses sender-eligible refund and void in one per-stream batch, with current role/preflight checks and receipt events. Recipient-only rights do not imply sender refund rights. Both state changes need reviewed authority; a user asking to pause has not chosen void. Indexer aliases are not contract evidence.

[Flow deployments](https://docs.sablier.com/guides/flow/deployments) provide version-specific addresses. Read chain code and exact contract methods before constructing a call; avoid hardcoded addresses from old recipes.

## Lockup and airdrops

[Lockup creation integration](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-create-vesting/references/evm-onchain.md) describes Linear, Dynamic and Tranched schedules, timestamp and duration variants, approvals and batching. Prefunded amount and schedule must match the user's obligation; timestamps are not interchangeable with durations.

[Cancelability](https://docs.sablier.com/concepts/cancelability) explains refund of eligible unvested funding and preserved vested rights. Read current cancelable state and present the effect before irreversible cancellation or renunciation. Transferable recipient NFTs can change who owns withdrawal rights.

[Airdrop skills](https://github.com/sablier-labs/sablier-skills/blob/main/skills/sablier-create-airdrop/SKILL.md) separate Merkle distribution from token vesting. Validate chain/module, root, recipient allocations, funding, claim window and clawback rights. A valid Merkle proof is not a claimed payout. Resolve claimed stream rights independently.
