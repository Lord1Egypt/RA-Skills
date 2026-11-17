## Description:

Helps agents research Amazon selling opportunities with APIClaw data for product selection, market analysis, competitor lookup, review analysis, pricing, risk assessment, and listing optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-srp](https://clawhub.ai/user/ryan-srp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and ecommerce operators use this skill to answer Amazon seller research questions, including market validation, ASIN lookup, product selection, competitor comparison, review insight, pricing, operational monitoring, and listing optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon research queries are sent to APIClaw.

Mitigation: Review the sensitivity of queries before use and install only if sending Amazon research data to APIClaw is acceptable.

Risk: API keys can be saved in a plaintext config file.

Mitigation: Use APICLAW_API_KEY as an environment variable and avoid giving the agent an API key to save automatically.

Risk: The Chinese seller workflow could support decisions based on nationality or inferred origin.

Mitigation: Avoid nationality-based decision criteria and rely on objective product, market, pricing, review, and seller-performance metrics.

## Reference(s):

- [APIClaw API Reference](references/reference.md)
- [Composite and Case Study Scenarios](references/scenarios-composite.md)
- [Product Evaluation Scenarios](references/scenarios-eval.md)
- [Pricing and Listing Scenarios](references/scenarios-pricing.md)
- [Daily Operations Scenarios](references/scenarios-ops.md)
- [Expansion and Iteration Scenarios](references/scenarios-expand.md)
- [Listing Optimization Scenarios](references/scenarios-listing.md)
- [APIClaw OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec)
- [APIClaw API Keys](https://apiclaw.io/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/ryan-srp/skills/apiclaw-analysis-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, concise analysis, API usage summaries, and inline shell commands when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APICLAW_API_KEY; full-mode analyses include data source and API usage blocks.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
