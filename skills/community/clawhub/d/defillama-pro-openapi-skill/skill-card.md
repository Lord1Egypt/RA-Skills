## Description:

Operate DefiLlama Pro analytics APIs through UXC with a curated OpenAPI schema, path-templated API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure UXC access to DefiLlama Pro and run read-only analytics queries for protocol TVL, chain metrics, token prices, yields, and stablecoin dominance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DefiLlama Pro API key is placed in request paths and may be exposed through shell history, verbose output, or daemon logs.

Mitigation: Configure credentials with environment variables or a secret manager, avoid literal secrets in commands, avoid verbose logging, and sanitize or delete logs after troubleshooting.

Risk: The linked OpenAPI schema controls which operations the agent exposes through UXC.

Mitigation: Verify the schema source before linking when reproducible reviewed behavior is required.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/defillama-pro.openapi.json)
- [DefiLlama API Docs](https://defillama.com/docs/api)
- [DefiLlama Pro Docs](https://defillama.com/pro-api/docs)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/defillama-pro-openapi-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash commands and API operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance targets read-only JSON API responses from DefiLlama Pro through UXC.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
