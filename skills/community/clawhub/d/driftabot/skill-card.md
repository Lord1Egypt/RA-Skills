## Description:

Query the DriftaBot Registry for API spec drifts, breaking changes, and provider information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pgomes13](https://clawhub.ai/user/pgomes13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check tracked API providers for spec drift, breaking changes, current spec locations, and supported spec types such as OpenAPI, GraphQL, and gRPC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry-derived summaries may be incomplete, stale, or different from an API provider's official guarantee.

Mitigation: Confirm important API decisions against the provider's canonical specifications or documentation.

Risk: The skill directs the agent to fetch public remote YAML and Markdown files.

Mitigation: Treat fetched registry content as reference data and review results before using them in production workflows.

## Reference(s):

- [DriftaBot Registry](https://driftabot.github.io/registry/)
- [DriftaBot Registry GitHub Repository](https://github.com/DriftaBot/registry)
- [DriftaBot Raw Registry Base URL](https://raw.githubusercontent.com/DriftaBot/registry/main)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with registry-derived provider, drift, and spec details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public registry files; no credentials or local system changes are requested by the skill evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
