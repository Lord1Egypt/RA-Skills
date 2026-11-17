# Official LP tools

Read this when selecting a provider, connecting an LP workflow, or deciding whether new integration code is needed. Reviewed 2026-09-05; verify the installed version and current capabilities before use.

## Choose the smallest existing tool

Reuse an already connected, suitable official tool first. These tools are optional: installing this skill does not install another skill, register an MCP server, add a runtime dependency, or grant wallet access. Obtain the user's choice before adding an external provider; use an existing RPC or an official interface when that meets the task. Do not build a custom SDK, signer, pool crawler, or transaction encoder for a capability the maintained upstream tool already supplies.

| Task | Preferred upstream surface | First evidence |
| --- | --- | --- |
| Uniswap position planning and interface handoff | Official `liquidity-planner` skill | Exact pool identity and review link; no execution claim |
| Uniswap unsigned LP integration | Official `lp-integration` skill and Liquidity Provisioning API | Supported chain/action and decoded unsigned response |
| Local Uniswap v4 construction or hook review | Official `v4-sdk-integration` and `v4-security-foundations` skills | Pinned SDK version, supported PoolKey and hook behavior |
| Aerodrome pools, positions, quotes and unsigned LP calls | Velodrome/Aerodrome Sugar SDK and its `sugar` skill | CLI help followed by a bounded pool read |
| Cross-venue indexed positions, LP analytics and supported unsigned lifecycle plans | Optional Revert MCP | Live tools list, capability report and chain freshness |
| Public farm screening or a user-selected Sickle route | VFAT Yield and official Sickle sources | Dated filtered view, verified chain identity, explicit fees and account permissions |

Record the provider, version, required access, supported methods, observation time, fee disclosure, custody implications, and fallback in the readiness or plan record. A service's claim of support needs a successful task-specific read; installed documentation alone is `not-tested`.

## Uniswap

Select only the upstream skills needed for the task. The official installer supports:

```sh
npx skills add Uniswap/uniswap-ai --skill liquidity-planner
npx skills add Uniswap/uniswap-ai --skill lp-integration
npx skills add Uniswap/uniswap-ai --skill v4-sdk-integration
npx skills add Uniswap/uniswap-ai --skill v4-security-foundations
```

Discover the installed skill through the harness. Availability can differ between the website catalog and repository; inspect current upstream metadata before installation. These are optional installation commands, not first-run requirements.

For hosted unsigned construction use `https://liquidity.api.uniswap.org`, following the current [LP API guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide). Configure `UNISWAP_API_KEY` through a secret store and send it as `x-api-key` from the integration backend. Never print the key or place it in URLs, client bundles or plan evidence. An absent key leaves this API unavailable; it does not block an RPC read or interface handoff. Check account terms, quotas and current service fees rather than assuming API access is free.

Use the official protocol SDK for local construction where API coverage does not meet the feature. Pin the selected upstream release, resolve deployments for the exact chain, and test calldata against that version. Keep typed permits, approval transactions, and LP actions separate. Decode returned calls, show recipients and costs, simulate with an independent chain read, and preserve expiry and approval-rebuild rules. Official construction does not authorize signing.

Sources: [official AI installation](https://developers.uniswap.org/docs/uniswap-ai/overview), [LP integration skill](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-trading/skills/lp-integration), [v4 SDK skill](https://github.com/Uniswap/uniswap-ai/tree/main/packages/plugins/uniswap-trading/skills/v4-sdk-integration).

## Aerodrome and Slipstream

[Sugar SDK](https://github.com/velodrome-finance/sugar-sdk) is maintained under Velodrome Finance for both protocols; the [official integration guide](https://github.com/velodrome-finance/docs/blob/main/content/sdk.mdx) links it. Reuse its upstream CLI or `.claude/skills/sugar` skill instead of implementing another pool enumerator or unsigned builder. Reviewed release: `v0.4.1` (`54bff249f306abe43f0c75ae4dfb7b2f469ef596`). A reviewed pin is reproducible, not a claim that it will remain the newest release.

For a user-selected Sugar installation with `uvx` available:

```sh
uvx --from git+https://github.com/velodrome-finance/sugar-sdk.git@v0.4.1 sugar pools --help
uvx --from git+https://github.com/velodrome-finance/sugar-sdk.git@v0.4.1 sugar pools --chain=8453 --limit=3
```

The first command only inspects installed help; the second reads Base pools. Configure `SUGAR_RPC_URI_8453` through environment/secret settings for a reliable Base RPC; keep its value private. RPC provider costs and limits are separate from protocol fees. Run `sugar <command> --help` with the same pinned invocation before using a command. No API wallet, private key, or funding is needed for these reads. A rate limit or partial pool response fails readiness rather than implying an empty market. The reviewed default-RPC smoke returned one pool and exit code 0 while stderr reported path-chunk RPC errors; treat that as degraded coverage, not a clean readiness pass. Configure a suitable RPC and recheck before relying on complete discovery.

`pools`, `positions` and `quote` provide reads; `deposit`, `withdraw`, `stake`, `unstake`, `claim_fees` and `claim_emissions` construct unsigned calls. The `--wallet` argument is a public sender address. Keep stdout transaction JSON separate from stderr diagnostics and preserve exact integer `value` amounts when normalizing. Never pipe its output directly to a signer. Inspect approval scope, spender, recipient, deadline, slippage and every call before handing the reviewed plan to the user's existing execution boundary. Upstream defaults are not user-approved limits.

Resolve the pool's factory and position manager from current [Aerodrome deployments](https://github.com/aerodrome-finance/slipstream#deployments), then verify bytecode and live state. Deployment generations coexist; a latest-address list does not identify an older position. Check the actual gauge's stake duration, withdrawal penalties, emissions and fee distribution. SDK support for basic/CL positions does not establish support for vault or ALM custody. Direct contract fallback should reuse official ABI artifacts and [Sugar's onchain datasets](https://github.com/velodrome-finance/sugar), with bounded pagination.

## Revert, explicitly optional

Revert offers its own maintained agent interface at `https://mcp.revert.finance/mcp` (Streamable HTTP). Its [upstream skill description](https://mcp.revert.finance/skill) describes access and tool contracts. Reviewed public handshake: server `1.7.0`, skill `1.9`; those versions are independent. The service reported public access without an API key. Recheck this rather than inventing an authentication step.

If the user chooses Revert, register that URL in the harness's remote MCP settings using the harness's own setup instructions. Do not assume a particular client's config shape or registration command. Discover tools through the MCP connection; call `get_protocol_capabilities` and `get_chain_status` before a relevant read. Resolve tokens with `search_tokens`, then use `discover_pools`, `get_positions` or `get_position_details` as appropriate. Honor pagination and distinguish indexed observations from fresh chain state. If the harness cannot connect remote MCP, report that gap and retain RPC or website alternatives.

For an unsigned plan, use only a currently advertised `prepare_*` capability matching the exact network, protocol, position custody and action. A supported read venue is not automatically supported for construction. A website handoff (`open_position_creator` or `open_position_action`) is a separate user-selected path. Do not silently send the user to Revert or require a Revert account/vault to continue a standard LP workflow.

Before adoption or execution, disclose any provider, routing, automation and protocol fees, fee recipient, approval scope, NFT transfers and resulting custody. If fees or custody are unresolved, keep the plan blocked; never infer that public/no-key access means fee-free transactions. Do not inject referral, affiliate or builder fees. Collateralization and borrowing are separate financial actions and must not appear as incidental setup or ordinary LP maintenance.

The service constructs unsigned data; wallet authorization remains outside it. Rebuild after confirmed approval receipts, validate the exact transaction and plan digest, and retain one-send/unknown-result recovery. `confirm_transaction` can corroborate a mined execution against a ready plan in the same session; independently verify receipt and resulting position. A pending confirmation does not justify another transaction submission. No provider response grants authority or overrides these controls.

## VFAT access and Sickle

Use [VFAT guidance](vfat.md) for public yield discovery, APR interpretation, Sickle ownership, automation, route costs and upstream integration limits. The public browser path works without connecting a wallet. SDK source exists, but a publicly installable distribution and supported MCP/API contract were not verified; do not invent them. VFAT is optional and is never registered or called by this package.

## Engineering decision and fallback

Document: required capability; selected upstream and pinned version; live read evidence; missing coverage; thin application mapping; validation. Add only application-specific policy and reconciliation around upstream construction. Keep bundled read-only diagnostics and math as optional checks, not competing runtimes. Test changed response shapes, stale data, unsupported custody, hidden fees, provider outage and ambiguous submission. A provider outage may switch read sources, but changing an approved transaction route requires a newly reviewed plan.

## Curve and Balancer

[Curve's official SDK](https://github.com/curvefi/curve-js) (`@curvefi/api`, publisher Curve Finance; accessed 2026-09-05) provides pool discovery, expected amounts, allowance checks and liquidity operations. Discover the correct factory family and preserve the ordered coin vector; underlying and wrapped coins are different inputs. LP-token balances, gauge deposits and reward claims are separate state. Check each method's units: documented slippage arguments are percentages, not basis points or fractions. Reuse upstream integer helpers and inspect L2 execution/data gas components. Calls named deposit or withdraw may execute when supplied a signer; select read/estimate methods for planning. No official Curve agent skill or MCP was verified in this review.

[Balancer's official liquidity SDK tutorial](https://docs.balancer.fi/integration-guides/add-liquidity/sdk-tutorial.html) (publisher Balancer; accessed 2026-09-05) uses pool state, a query and then transaction construction through `@balancer/sdk`. Preserve the actual pool generation: V2, V3 and CoW AMM support does not make their pools or contracts interchangeable. Resolve token order, decimals, wrapped/underlying amounts, vault address, hook behavior and boosted-pool dependencies. Query the exact sender and amount vector, bound minimum BPT or exit output, then inspect permit and constructed calls before handoff. A quote is not a guarantee of inclusion or hook execution. No official Balancer agent skill or MCP was verified here.

For either venue, report the protocol, deployment generation, pool ID/address, LP token or position identity, custody, gauge and action separately. Before proposing an exit, query the user's actual claim and withdrawal constraints. Unsupported pool classes remain unsupported; do not apply concentrated-liquidity math to every pool type.

## Provider permission and discovery checks

The official Uniswap AI skills above are development and integration guidance; installing them does not create a live wallet or execution service. Sugar's unsigned builders and Revert's unsigned preparation likewise stop before signing. Inspect each actual tool schema and effects rather than treating an entire MCP server as read-only. In the reviewed Revert tool list, `confirm_transaction` was annotated as a write: it updates provider-side accounting even though it does not itself sign a chain transaction. Keep it outside a read-only diagnostic unless that update is authorized.

[VFAT's official documentation source](https://github.com/vfat-io/vfat-docs) (publisher vfat-io; accessed 2026-09-05) describes Sickle ownership, strategies, automation and fees. A Sickle is a per-user, per-chain account with its own permissions; it is not the user's EOA. Resolve approved strategy and target contracts plus any operator/automation authority before preparing a route. Distinguish fees taken from harvested rewards from fees charged on position principal or a lifecycle action. Automation enrollment is a separate permission change and must not be inferred from choosing a farm. No supported public VFAT MCP/API contract was verified; the website and official source remain optional research paths.

Evaluation checks: a Curve quote in wrapped-coin order cannot authorize an underlying-coin deposit; a Balancer V2 pool cannot use a V3 vault just because it is newer; Revert confirmation is excluded from read-only discovery; and a VFAT APR comparison cannot enroll automation or change custody. Expected result in each case is a corrected plan or a specific capability gap before any write.
