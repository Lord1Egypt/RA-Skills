## Description:

Canadian Tire product data as structured JSON at the store you choose - search by keyword or category with that store's price and stock, full product detail, price and stock for up to 50 SKUs in one call, a store locator with per-store stock and aisle, and each store's clearance and deals (sale, instant rebate, special buy, Triangle Rewards). 6 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up Canadian Tire products, store-specific prices and inventory, nearby store availability, clearance items, and deals. It helps compare options using current results for a selected Canadian Tire store.

### Deployment Geography for Use:

Canada

## Known Risks and Mitigations:

Risk: Requests and any supplied store location are received by Scavio.

Mitigation: Use a postal-code prefix or a known store ID when sufficient.

Risk: API usage consumes credits and may incur charges after the included balance.

Mitigation: Track credit use and review the per-request cost before repeated lookups.

Risk: An exposed API key could be used by others.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store, not in source control.

Risk: Optional SDK and MCP setup adds external packages and connected tools.

Mitigation: Review those packages separately and enable only the MCP platforms you need.

## Reference(s):

- [Canadian Tire API overview](https://scavio.dev/canadiantire-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Product endpoint documentation](https://scavio.dev/docs/canadiantire-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Search endpoint documentation](https://scavio.dev/docs/canadiantire-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Store locator documentation](https://scavio.dev/docs/canadiantire-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Availability endpoint documentation](https://scavio.dev/docs/canadiantire-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Clearance endpoint documentation](https://scavio.dev/docs/canadiantire-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Deals endpoint documentation](https://scavio.dev/docs/canadiantire-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)
- [Rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [Structured JSON product, price, inventory, store, clearance, and deal data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are tied to the selected store; each endpoint call uses 1 credit.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
