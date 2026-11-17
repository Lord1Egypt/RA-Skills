## Description:

Amazon product research and seller analytics for FBA and FBM businesses, including product selection, competitor tracking, BSR monitoring, review analysis, monthly sales estimates, listing optimization, and market opportunity assessment using the APIClaw API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christine-srp](https://clawhub.ai/user/christine-srp)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agent users use this skill to research Amazon products, compare competitors, assess market risk, estimate sales, plan pricing, and draft or optimize listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext credential handling may expose the APIClaw API key if users ask an agent to save it to config.json.

Mitigation: Prefer APICLAW_API_KEY as an environment variable or managed secret, and avoid writing API keys to disk.

Risk: Product research queries and business-sensitive criteria are sent to APIClaw.

Mitigation: Share only the product, category, and marketplace details needed for the task, and review APIClaw data handling expectations before use.

Risk: The Chinese-seller workflow can encourage nationality-based seller profiling beyond ordinary competitor research.

Mitigation: Avoid that workflow or rewrite it around neutral competitor-performance criteria such as pricing, fulfillment, reviews, and sales signals.

Risk: The README's npx installer is unpinned.

Mitigation: Use a reviewed package version or manual installation path when deploying in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christine-srp/skills/amazon-seller-research)
- [APIClaw API](https://apiclaw.io)
- [APIClaw API key setup](https://apiclaw.io/api-keys)
- [APIClaw OpenAPI specification](https://apiclaw.io/api/v1/openapi-spec)
- [APIClaw API Reference](references/reference.md)
- [Amazon Seller Comprehensive Analysis & Case Studies](references/scenarios-composite.md)
- [Amazon Product Evaluation & Risk Assessment](references/scenarios-eval.md)
- [Amazon Pricing Strategy & Profit Estimation](references/scenarios-pricing.md)
- [Amazon Seller Daily Operations & Monitoring](references/scenarios-ops.md)
- [Amazon Product Expansion & Market Trends](references/scenarios-expand.md)
- [Amazon Listing Optimization & Content Creation](references/scenarios-listing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline shell commands; API command results are JSON inputs to the agent's analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APICLAW_API_KEY and sends product research queries to the APIClaw API.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter reports 1.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
