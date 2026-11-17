## Description:

Helps agents extract product details from store pages and compare marketplace listings through ToolRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blakefolgado](https://clawhub.ai/user/blakefolgado)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, researchers, and resale sellers use the skill to compare product prices, inspect listings, and monitor marketplace snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, queries, and scraped content are shared with ToolRouter.

Mitigation: Avoid internal, login-protected, regulated, or confidential pages without approval.

Risk: The MCP package introduces a third-party setup dependency.

Mitigation: Review or pin the package before use.

Risk: Product images may be saved to local file space by default.

Mitigation: Set include_images:false when images are not needed.

## Reference(s):

- [E-commerce Scraper release](https://clawhub.ai/blakefolgado/skills/ecommerce-scraper)
- [ToolRouter product scraper](https://toolrouter.com/tools/product-scraper)
- [ToolRouter quickstart](https://toolrouter.com/docs/markdown/quickstart)
- [ToolRouter marketplace search](https://toolrouter.com/tools/marketplace-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and price comparison tables with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes currencies and retrieval dates; product images may be saved locally if enabled.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
