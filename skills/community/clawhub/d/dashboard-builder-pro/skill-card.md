## Description:

Dashboard Builder Pro helps teams create local multi-source dashboards with templates, visual QA checks, and alert configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and data teams use this skill to ask an agent for local operational dashboards that combine API, database, and file sources. It can also guide generation of dashboard scripts, template reuse, QA checks, and threshold-based alert configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell or Python scripts may run with local file, network, or database access.

Mitigation: Review each generated script before execution and run it with the narrowest practical local permissions.

Risk: Dashboard workflows may require API keys, database URLs, or other sensitive credentials.

Mitigation: Use read-only and narrowly scoped credentials, keep secrets in environment variables or a secret manager, and do not commit .env files.

Risk: Dashboard files or generated outputs may expose sensitive operational data.

Mitigation: Inspect generated dashboards before sharing and avoid publishing outputs that contain secrets, personal data, or confidential metrics.

Risk: Alert webhooks can send operational details to unintended destinations.

Mitigation: Confirm webhook destinations and payload contents before enabling alert rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dashboard-builder-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local dashboard files, data-fetch scripts, QA commands, and alert configuration for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
