## Description:

ALDI grocery data as structured JSON at the store you choose - search ALDI US with that store's price, sale price, unit price, stock level and in-store location, for in-store, pickup or delivery pricing; read one product with ingredients, allergens and dietary labels; and find ALDI stores near a ZIP. 3 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to look up ALDI US products, store-specific prices and stock levels, product details, and nearby stores for grocery planning and price comparisons.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ZIP code, selected store, and grocery searches are sent to Scavio; external SDK/MCP implementations and Scavio data-retention practices were not verified.

Mitigation: Share only the location and search details needed for the lookup, and review applicable privacy and retention terms before use.

Risk: The API key grants access to the Scavio account, and requests consume account credits.

Mitigation: Keep the key in an environment variable or secret store and monitor credit usage.

## Reference(s):

- [Scavio ALDI API overview](https://scavio.dev/aldi-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data)
- [ALDI search documentation](https://scavio.dev/docs/aldi-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data)
- [ALDI product documentation](https://scavio.dev/docs/aldi-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data)
- [ALDI stores documentation](https://scavio.dev/docs/aldi-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data)

## Skill Output:

**Output Type(s):** [Structured JSON, Guidance]

**Output Format:** [Structured JSON records with concise explanatory text as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and stock are specific to the selected store and shopping mode; stock is reported as a level, not a quantity.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
