# Uniswap integration surfaces

Select one primary transaction-construction path per feature. Do not mix response contracts or approval assumptions across paths.

## Interface handoff

Use an interface deep link when the product should hand final review and transaction construction to the Uniswap app. Generate the link from bound addresses and range terms, show it to the user, and treat every value displayed by the app as a fresh proposal. Deep-link query parameters are an interface contract and can change without an onchain deployment.

This path is not programmatic execution. Completion still requires a receipt and state reconciliation if the surrounding product tracks the action.

## Liquidity Provisioning API

Use the official LP API when the application needs server-built unsigned transactions for v2, v3, or v4. Verify the current OpenAPI or service contract and integration guide. The reviewed routes cover approval checks, classic and concentrated creation, increase, decrease, fee claims, and pool reads.

Model the response rather than erasing its quirks:

- `transactions[].transaction` wraps approval transactions.
- Approval checks can return both onchain transactions and typed permit data.
- Permission or KYC warnings are a blocking result even when no approval transaction is returned.
- Amounts are integer base-unit strings.
- Position ID and permit field names vary by endpoint.
- Tick-snapped adjusted prices are distinct from requested prices.
- v3 decrease calldata can bundle fee collection.
- v4 fee collection can be expressed as a zero-liquidity modification and token-taking actions.
- API `requestId` should be retained for observability and support.

Keep the API client in the unsigned-builder layer. It must not hold keys, sign, submit, or share a generic retry wrapper with wallet writes. Validate all returned targets and calldata against locally resolved deployments, decode nested calls, simulate independently, and enforce plan freshness.

For a v4 batch permit, normalize the proto-shaped typed data only in the wallet adapter used for signing. Verify the numeric chain ID, domain, verifying contract, types, values, spender, amounts, nonce, and expiry. Keep the original payload for the subsequent API request. Support a permit-as-transaction path only when it receives the same approval review.

Do not hardcode the supported chain set. Discover current capability from official documentation or a harmless API probe and return typed `unsupported` when absent.

## Direct SDK path

Use current official protocol SDKs when local construction, fork testing, or custom behavior is required.

- v2 uses pair reserve math and fungible LP tokens.
- v3 uses pool and position math plus the NonfungiblePositionManager lifecycle.
- v4 uses the complete PoolKey, StateView for pool reads, PositionManager actions for LP lifecycle, native currency support, Permit2, and hook-aware settlement.

Resolve deployment addresses for the exact chain from current official registries and verify bytecode. Position discovery may use indexed PositionManager events; ownership and live position state must be reconciled onchain before action.

## Shared test contract

Cover direct SDK, API, and interface handoff separately. Test:

- wrong chain, token order, price orientation, decimals, pool reference, hook, and position ID
- empty data, wrong wrapper field, stale request, changed adjusted price, and unexpected target
- approval transactions plus permit in the same response
- typed-data chain and type normalization without mutating the payload returned to the API
- permission and KYC warnings
- v2 classic creation and rejection of v2 fee claims
- v3 decrease with bundled fee collection
- v4 StateView reads, event-based discovery, native currency, nested actions, and zero-liquidity fee collection
- rate limiting and builder outages without duplicate wallet submission
- receipt success with an unexpected state diff

Current primary references:

- [Uniswap AI skills](https://developers.uniswap.org/docs/uniswap-ai/skills)
- [Uniswap AI LP integration](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-trading/skills/lp-integration)
- [Uniswap AI v4 SDK integration](https://github.com/Uniswap/uniswap-ai/blob/main/packages/plugins/uniswap-trading/skills/v4-sdk-integration/SKILL.md)
- [Uniswap LP API guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide)
