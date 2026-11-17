## Description:

CVS product data as structured JSON - search cvs.com front-store products with regular and sale price, unit price, promotion, ExtraBucks rewards and manufacturer coupons, and units in store and for pickup at the store you choose; read one product with UPC, ingredients, directions, warnings and variants; and check stock for up to 20 SKUs at one store. 3 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to search CVS front-store products, compare listed prices and coupons, inspect product details, and check inventory for a selected store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, product selections, and store numbers are sent to Scavio; requests consume API credits.

Mitigation: Avoid including personal medical details, keep SCAVIO_API_KEY in secret storage, and monitor credit use.

Risk: Enabling the optional MCP integration adds tools and saved credentials.

Mitigation: Review the additional MCP tools and protect saved credentials.

## Reference(s):

- [Scavio CVS API overview](https://scavio.dev/cvs-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data)
- [CVS search endpoint documentation](https://scavio.dev/docs/cvs-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data)
- [CVS product endpoint documentation](https://scavio.dev/docs/cvs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data)
- [CVS stock endpoint documentation](https://scavio.dev/docs/cvs-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON product, price, coupon, and store-stock data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint responses include product and stock fields; each call uses one API credit.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
