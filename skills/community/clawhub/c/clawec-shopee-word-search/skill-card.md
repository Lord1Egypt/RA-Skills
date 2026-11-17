## Description:

ClawEC API helper for querying Shopee hot-search keyword lists by site and optional category, including search index, 30-day sales and GMV, recommended bid, and product-count metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operators use this skill to query ClawEC's Shopee keyword data, compare demand and competition metrics, and choose keywords for category research, listings, and advertising.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected Shopee site, category, filter, and date parameters in CLAWEC_API_KEY-authenticated requests to clawec.com.

Mitigation: Use it only when Clawec is an intended data provider, keep CLAWEC_API_KEY in an environment variable, and review query parameters before running the helper script.

## Reference(s):

- [Shopee word search response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-word-search)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with keyword tables, API error notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are normally in Chinese and may include query conditions, Shopee keyword metrics, opportunity analysis, and 3-5 recommended keywords.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
