## Description:

Finds winning Amazon products with product-selection strategies, market and competitor analysis, review insights, pricing guidance, listing optimization, and risk assessment using APIClaw data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-srp](https://clawhub.ai/user/ryan-srp)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and agent operators use this skill to research Amazon categories, select products, compare competitors, estimate pricing, analyze reviews, optimize listings, and assess product risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored in plaintext config files if the environment variable is not used.

Mitigation: Set APICLAW_API_KEY as an environment variable and avoid giving persistent secrets to the agent.

Risk: Amazon research queries, ASINs, categories, competitor targets, and review targets are sent to APIClaw.

Mitigation: Use the skill only when sharing those inputs with APIClaw is acceptable for the user's data-handling requirements.

Risk: The Chinese seller workflow can encourage nationality profiling when location data is missing.

Mitigation: Rely only on explicit seller location fields and avoid inferring nationality from names, brands, or stereotypes.

Risk: Some market and trend outputs are based on current snapshots, not historical time series.

Mitigation: Treat growth and anomaly findings as directional, and compare repeated snapshots before making high-impact decisions.

Risk: Installation or execution from an unverified source could run unexpected code.

Mitigation: Verify the installer source or use a pinned installation path before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryan-srp/skills/amazon-analysis-skill)
- [APIClaw](https://apiclaw.io)
- [APIClaw API Keys](https://apiclaw.io/api-keys)
- [APIClaw OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec)
- [APIClaw API Reference](references/reference.md)
- [Composite Product Recommendation Scenarios](references/scenarios-composite.md)
- [Product Evaluation Scenarios](references/scenarios-eval.md)
- [Pricing and Listing Scenarios](references/scenarios-pricing.md)
- [Daily Operations Scenarios](references/scenarios-ops.md)
- [Expansion and Iteration Scenarios](references/scenarios-expand.md)
- [Listing Optimization Scenarios](references/scenarios-listing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, API usage summaries, data-source notes, and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APICLAW_API_KEY; normal outputs include analysis, recommendations, and traceability notes rather than raw data exports.]

## Skill Version(s):

0.1.6 (source: server-resolved ClawHub release metadata; artifact frontmatter reports 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
