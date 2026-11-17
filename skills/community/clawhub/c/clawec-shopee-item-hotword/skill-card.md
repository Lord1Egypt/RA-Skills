## Description:

Queries Shopee item hot search words through the ClawEC API, including traffic keywords, category hotwords, search index, recent 30-day sales and GMV, and recommended bid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, ecommerce analysts, and agent developers use this skill to retrieve Shopee keyword demand signals for up to 10 item IDs and turn the results into SEO or advertising keyword recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee item IDs, site and type parameters, optional dates, and a ClawEC bearer token to clawec.com.

Mitigation: Install only when that data sharing is acceptable, store the token in CLAWEC_API_KEY, and review ClawEC account and API terms for marketplace data handling.

Risk: Invalid parameters or failed API responses can produce incomplete keyword analysis.

Mitigation: Validate site, type, item ID count, and optional yyyy-MM-dd date before calling the API, then check both top-level status and data.success before using results.

Risk: Keyword recommendations may be misleading if search index, sales, GMV, product count, and bid price are read in isolation.

Mitigation: Sort and compare multiple returned fields and present prioritized recommendations with the query scope and assumptions.

## Reference(s):

- [Response Schema](references/response-schema.md)
- [ClawEC API Base](https://www.clawec.com/api)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-item-hotword)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, keyword opportunity notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report language is Chinese; API requests require site, itemIds, type, and optionally timest.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
