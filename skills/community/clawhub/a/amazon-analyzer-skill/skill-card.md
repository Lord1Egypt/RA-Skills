## Description:

Find winning Amazon products with 14 selection strategies and 6-dimension risk assessment backed by APIClaw's Amazon product database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyle-srp](https://clawhub.ai/user/kyle-srp)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, analysts, and developers use this skill to query APIClaw for Amazon category, product, competitor, pricing, review, and listing data, then produce seller-facing product research and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored in plaintext config.json when provided to the agent.

Mitigation: Set APICLAW_API_KEY as an environment variable and avoid pasting the key into the agent unless local plaintext storage is intentional.

Risk: The Chinese-seller case-study workflow can encourage weak nationality inference from seller or brand patterns.

Mitigation: Use only explicit sellerLocation data for location-based analysis, or present the workflow as neutral competitor analysis when location data is missing.

Risk: An unpinned install command can make the installed package differ from the reviewed release.

Mitigation: Verify the package or source version before installation and deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyle-srp/skills/amazon-analyzer-skill)
- [APIClaw API Reference](references/reference.md)
- [APIClaw OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec)
- [Composite Recommendation Scenarios](references/scenarios-composite.md)
- [Product Evaluation and Risk Scenarios](references/scenarios-eval.md)
- [Pricing Scenarios](references/scenarios-pricing.md)
- [Operations Scenarios](references/scenarios-ops.md)
- [Expansion Scenarios](references/scenarios-expand.md)
- [Listing Scenarios](references/scenarios-listing.md)
- [API Key Setup](https://apiclaw.io/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with inline shell commands and JSON API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APICLAW_API_KEY for live API calls; full analyses include data source and condition notes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
