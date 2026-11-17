## Description:

Amazon product research and seller analytics for FBA and FBM businesses, including product selection, competitor tracking, BSR trend monitoring, review analysis, sales estimation, listing optimization, and market opportunity assessment using APIClaw data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christine-srp](https://clawhub.ai/user/christine-srp)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agent users use this skill to research Amazon products, compare competitors, estimate demand, assess category risks, and draft or optimize listings. It is intended for explicit Amazon seller analytics workflows that can use a configured APIClaw account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid or sensitive APIClaw account through APICLAW_API_KEY.

Mitigation: Load APICLAW_API_KEY from a secure environment or secret manager, avoid pasting keys into normal chat, and do not store keys in the skill directory.

Risk: Workflows that identify Chinese sellers or infer seller origin from names can produce biased or inaccurate results.

Mitigation: Treat seller-origin analysis as uncertain, review outputs before acting on them, and avoid using inferred nationality as the sole decision factor.

Risk: Bulk API calls can consume account quota or incur cost.

Mitigation: Confirm with the user before bulk lookups and keep requests scoped to the ASINs or categories needed for the task.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/christine-srp/skills/apiclaw-analysis)
- [APIClaw](https://apiclaw.io)
- [APIClaw API Key Setup](https://apiclaw.io/api-keys)
- [APIClaw OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec)
- [APIClaw API Reference](references/reference.md)
- [Amazon Seller Comprehensive Analysis & Case Studies](references/scenarios-composite.md)
- [Amazon Product Evaluation & Risk Assessment](references/scenarios-eval.md)
- [Amazon Pricing Strategy & Profit Estimation](references/scenarios-pricing.md)
- [Amazon Listing Optimization & Content Creation](references/scenarios-listing.md)
- [Amazon Seller Daily Operations & Monitoring](references/scenarios-ops.md)
- [Amazon Product Expansion & Market Trends](references/scenarios-expand.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and API-derived analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured tables, product recommendations, risk matrices, API usage notes, and listing copy.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter reports 1.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
