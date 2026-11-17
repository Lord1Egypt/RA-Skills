## Description:

Provides Dollar General product search, store-level prices and stock, product details, nearby store availability, deals, and digital coupons as structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can look up Dollar General products by keyword or UPC, compare store-specific prices and availability, find nearby stores, and review current deals and coupons.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Searches and supplied location data are sent to Scavio, and requests consume API credits.

Mitigation: Prefer a ZIP code over precise coordinates when sufficient, and account for per-request credit use.

Risk: The API key can be exposed if copied into source code or shared configuration.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store and do not commit it to source control.

Risk: Optional SDK or MCP package behavior and the service's data-retention practices were not verified by the artifact review.

Mitigation: Review optional packages and the provider's data practices before enabling them; enable only the platforms needed when using MCP.

## Reference(s):

- [Dollar General API overview](https://scavio.dev/dollargeneral-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)
- [Product endpoint documentation](https://scavio.dev/docs/dollargeneral-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)
- [Search endpoint documentation](https://scavio.dev/docs/dollargeneral-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)
- [Store locator endpoint documentation](https://scavio.dev/docs/dollargeneral-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)
- [Deals endpoint documentation](https://scavio.dev/docs/dollargeneral-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)
- [Coupons endpoint documentation](https://scavio.dev/docs/dollargeneral-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=dollar-general-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise natural-language summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results are store-specific for prices and inventory; responses include current product, store, deal, or coupon data.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
