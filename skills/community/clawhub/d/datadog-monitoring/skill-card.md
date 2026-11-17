## Description:

Inspect Datadog monitors, metrics, logs, incidents, dashboards, and observability data - powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect and manage Datadog observability data from chat, including monitors, metrics, logs, incidents, dashboards, traces, and service dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an external ClawLink plugin and authorize Datadog access that may include sensitive reads and write operations.

Mitigation: Review the ClawLink plugin and requested Datadog OAuth scopes before installation; prefer a dedicated least-privilege Datadog account and avoid broad reconnects unless write operations are required.

Risk: Datadog logs, traces, users, roles, API-key metadata, webhooks, incidents, monitors, and host data can contain confidential operational information.

Mitigation: Treat retrieved observability data as confidential and limit access to users and workspaces approved for that Datadog organization.

Risk: Write tools can create, update, mute, unmute, or delete Datadog resources, including monitors and dashboards.

Mitigation: Require human confirmation for write and destructive operations, and verify target resource identifiers before execution.

## Reference(s):

- [ClawHub Datadog Skill Page](https://clawhub.ai/hith3sh/skills/datadog-monitoring)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=datadog-monitoring)
- [ClawLink Datadog Connection Dashboard](https://claw-link.dev/dashboard?add=datadog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route requests through ClawLink tools connected to the user's Datadog account]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
