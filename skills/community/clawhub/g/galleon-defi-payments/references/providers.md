# Official payment providers

Primary sources accessed 2026-09-05. These interfaces were researched from documentation; authenticated payments and stream execution were not tested.

| Provider | Official surface and access | Operational distinction |
|---|---|---|
| Coinbase / x402 | [Buyer SDK guide](https://docs.cdp.coinbase.com/x402/buyer/quickstart), official `coinbase/cdp-sdk` skill `build-x402-client`, CDP-managed or user-owned wallet | SDK guide uses Node 22+ and CDP credentials; its client can provision a wallet and automatically retry a paid request. Inspect configuration before running examples. Explicit development mode uses testnet; omitted environment can use mainnet. |
| x402 protocol | [Payment flow](https://docs.cdp.coinbase.com/x402/how-it-works), [official protocol](https://docs.x402.org/) | A server offers payment requirements; verification, work, settlement and response are separate stages. Discover supported scheme/network/asset; do not assume every facilitator supports every rail or only fixed-price USDC. |
| Sablier | [Official agent skills](https://docs.sablier.com/guides/ai-agents), [`sablier-labs/sablier-skills`](https://github.com/sablier-labs/sablier-skills), deployed contracts and subgraphs | Official skills cover vesting, open-ended streams, airdrops and withdrawals. Reuse the relevant upstream procedure after source review. No public runtime MCP established in this review. |
| Superfluid | [Official skills](https://github.com/superfluid-org/skills), [current skill source](https://raw.githubusercontent.com/superfluid-org/skills/main/skills/superfluid/SKILL.md) | Current app integrations use `@sfpro/sdk`; onchain contracts and metadata have separate packages. CFA is one-to-one flow; GDA is distribution via pools. IDA and older macro paths have replacement guidance. No official runtime MCP established here. |

## x402 access and evidence

For the current protocol contract, use [x402 v2 verification and recovery](x402-v2.md), reviewed 2026-09-21. The older provider-specific SDK examples below do not establish a universal default network or protocol version.

Do not run a generic payment-wrapped fetch merely to inspect a URL: the wrapper can sign/pay automatically. First establish an allowed HTTPS origin/resource, selected network/token, advertised amount or maximum, facilitator and payer. Reject changed terms, unsupported schemes and unexpected redirects. Use the official client's supported policy hooks and wallet controls; do not invent options that merely look plausible.

A CDP wallet secret is signing authority. Agentic Accounts, Agentic Wallets, Coinbase exchange portfolios and embedded wallets are different custody/access models. Use the existing account with its documented capabilities and isolate secrets using the host's native secret mechanism. Seller integration is a separate task: endpoint ownership, settlement destination, pricing and facilitator configuration need their own scope.

## Sablier models

[Flow](https://docs.sablier.com/concepts/flow/overview) tracks debt accruing at a rate per second and can be underfunded. Read covered and uncovered debt, withdrawable balance and the current recipient. Pausing preserves accrued debt; voiding is permanent and can forfeit uncovered debt. Do not report accrued debt as cash received.

[Lockup cancelability](https://docs.sablier.com/concepts/cancelability) controls recovery of unvested funds; vested rights remain with the recipient. Cancelling cannot be undone and renouncing cancellation cannot be reversed. Campaign clawback rules differ from the streams created by claims. Read the deployed product/version and claim window, rather than applying a fixed grace period to every campaign.

## Superfluid models

Load current official architecture/SDK references for the chosen track. Check real-time spendable balance, required deposit/buffer, current aggregate outgoing rate, flow operator permissions and projected exhaustion. An incoming flow can stop; it is not permanent collateral for an outgoing commitment. Wrapped Super Tokens and their underlying token have different amounts and permissions. Read current clear-signing macro guidance and inspect every action in a batch; a human-readable signature is not proof that all nested actions match the request.
