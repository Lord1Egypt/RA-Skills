## Description:

Analyzes competitor positioning and identifies whitespace opportunities for a product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinu4you](https://clawhub.ai/user/jinu4you)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this agent to compare a product against named competitors, generate competitor profiles, produce a comparison matrix, and summarize whitespace opportunities with a strategic recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product details, competitor names, search queries, retrieved snippets, and generated prompts may be sent to Tavily and the selected LLM provider.

Mitigation: Avoid sensitive inputs unless the provider terms are acceptable, and restrict API keys, quotas, and access to the minimum needed.

Risk: Generated competitive analysis can be influenced by incomplete web results or model errors.

Mitigation: Treat profiles, comparison rows, whitespace items, and recommendations as advisory and review them against trusted market sources before business use.

Risk: Provider credentials and dependencies require normal operational hygiene.

Mitigation: Keep API keys out of version control, rotate or scope keys where possible, and update dependencies during maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinu4you/skills/agent-compete-scope)
- [Publisher profile](https://clawhub.ai/user/jinu4you)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON response containing competitor profiles, a comparison matrix, whitespace items, and a markdown-formatted recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires product and competitor inputs; supports focus values for pricing, features, positioning, or all.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
