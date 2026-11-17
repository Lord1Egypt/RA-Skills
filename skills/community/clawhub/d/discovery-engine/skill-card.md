## Description:

Helps agents find and explain statistically validated patterns in tabular data, including subgroup effects, feature interactions, and literature-backed novelty assessments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessicarumbelow](https://clawhub.ai/user/jessicarumbelow)

### License/Terms of Use:

MIT

## Use Case:

Developers and data analysts use this skill to analyze tabular datasets with Disco and communicate validated patterns, effect sizes, and supporting citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An analysis may publish results publicly by default, exposing sensitive dataset insights.

Mitigation: Confirm visibility before every run and explicitly select private visibility for confidential data.

Risk: Selected datasets are sent to Disco's hosted service for analysis.

Mitigation: Only submit data approved for upload to that service and review its sensitivity first.

Risk: A payment-enabled API key can permit autonomous purchases, subscriptions, or payment-method changes without a hard confirmation gate.

Mitigation: Do not expose a payment-enabled key to autonomous workflows unless human approval is enforced for billing actions.

## Reference(s):

- [Discovery skill release](https://clawhub.ai/jessicarumbelow/skills/discovery-engine)
- [Disco documentation](https://disco.leap-labs.com/llms-full.txt)
- [Python SDK reference](docs/python-sdk.md)
- [OpenAPI specification](docs/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with structured pattern details and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pattern conditions, effect sizes, adjusted p-values, literature citations, and novelty classifications.]

## Skill Version(s):

0.2.182 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
