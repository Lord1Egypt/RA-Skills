## Description:

Queries Shopee category trend overviews through the Clawec API across multiple sites and monthly, quarterly, or yearly time ranges, including time series for sales volume, GMV, products, shops, and brands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agent developers use this skill to query Shopee category trend data, compare categories across supported Shopee sites, and produce concise Chinese market trend reports for product-selection validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee category trend query parameters to clawec.com using a CLAWEC_API_KEY.

Mitigation: Use environment storage for CLAWEC_API_KEY, do not hardcode the key, and avoid submitting sensitive business data beyond the query fields required.

Risk: API requests can fail because of missing credentials, invalid parameters, or unsuccessful business-layer responses.

Mitigation: Check the top-level status, data.success, errorCode, and errorMessage before interpreting trend data.

## Reference(s):

- [Shopee Category Trend Response Schema](artifact/references/response-schema.md)
- [ClawEC API Base](https://www.clawec.com/api)
- [Shopee Category Trend API Endpoint](https://www.clawec.com/api/aigc/ec/shopee/data/category/trend)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-category-trend)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Chinese Markdown report with trend tables, interpretation, conclusions, and optional bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEC_API_KEY for live API calls; results should be grouped by site and sorted by date.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
