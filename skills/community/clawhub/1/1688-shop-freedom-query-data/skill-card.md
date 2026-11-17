## Description:

1688 Shop Freedom Query Data converts natural-language merchant data questions into RAG-assisted 1688 API calls and returns authentic shop metrics with interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and their agents use this skill to query shop traffic, transaction, product, search, comparison, and review metrics from live 1688 data sources and receive a concise operational interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a 1688 merchant AK that may be stored in OpenClaw configuration or read from the environment.

Mitigation: Install and configure it only in a trusted OpenClaw profile, protect the local configuration file, and avoid using an untrusted OPENCLAW_GATEWAY_URL for configuration.

Risk: Returned shop metrics and generated HTML or Excel exports can contain sensitive business data.

Mitigation: Store exports only in approved locations, limit sharing, and remove exported files when they are no longer needed.

Risk: The visualization option may pass query results to another installed skill.

Mitigation: Review the selected visualization skill before forwarding results, or skip visualization when the downstream skill is not trusted.

## Reference(s):

- [Interaction Specs](references/interaction-specs.md)
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-shop-freedom-query-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with JSON command outputs; optional HTML or Excel files when export is selected.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses signed 1688 gateway API calls and may produce sensitive business-data exports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
