# VFAT access and readiness

Use VFAT as an optional public discovery interface or a user-selected position-management route. Reviewed 2026-09-05.

## Start without a wallet

Open [VFAT Yield](https://vfat.io/yield) with a public browser and wait for the table to finish loading. Record the selected Farms/Pools view, active filters, sort order, observation time and exact chain/protocol/pool. A loading shell or filtered empty table is not evidence of an empty market. The public page was verified to render farms without connecting a wallet; this does not verify its quotes or writes.

Use public address/ENS viewing only for an account the user selected. The [portfolio guide](https://docs.vfat.io/portfolio/) describes this read path. Do not connect a wallet, create a Sickle, or enable automation merely to inspect opportunities. A user address entered into a hosted service is visible to that provider.

## Choose a supported access path

- Public browser: inspect yield candidates and source links, then verify identity and economics with chain reads or a suitable existing protocol tool.
- Sickle contract reads: use current official ABIs with an existing RPC/ABI tool. Resolve the factory, Sickle, registry and deployed implementation for the intended chain; source constants are not a deployment registry.
- Integration source: [sickle-public](https://github.com/vfat-io/sickle-public) and [sickle-wrapper](https://github.com/vfat-io/sickle-wrapper) are official sources. The latter documents a wrapper SDK, but its reviewed manifest depends on a sibling local SDK. Both named public npm packages returned 404 during this review. Treat ready-to-install SDK access as unavailable until upstream publishes or supplies a verified distribution.

No supported public VFAT MCP or general quoting API contract was verified. Do not invent a server, authentication token, CLI command or endpoint from browser network traffic. Use a documented upstream interface when one becomes available; record the version and access terms before integration. For Aerodrome capabilities already served by the maintained Sugar SDK, retain that path rather than adopting VFAT's fork by default.

## Readiness result

Return `provider`, `accessPath`, `observedAt`, `viewAndFilters`, `chainAndPool`, `readEvidence`, `supportedOperations`, `missing`, and `nextAction`. Keep browser discovery, RPC verification, quote construction, wallet authority and automation permissions as separate capabilities. An official repository or an enabled button proves none of the others.

A VFAT route can use a user-owned Sickle smart contract account, or a separately chosen ownership wrapper. Establish the actual owner and approved operators from chain state before describing custody. [Sickle documentation](https://docs.vfat.io/sickle/) explains the basic account model; the live implementation remains authoritative.
