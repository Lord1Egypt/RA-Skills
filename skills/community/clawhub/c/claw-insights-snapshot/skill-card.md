## Description:

Generate visual status cards for an OpenClaw agent as PNG, SVG, or JSON for sharing operational status and extracting metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucal6](https://clawhub.ai/user/lucal6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create compact OpenClaw status snapshots for chat sharing, scheduled reports, and JSON metrics extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards and JSON may expose operational telemetry such as token usage, session activity, errors, gateway health, hostnames, or channel status.

Mitigation: Review generated snapshots before sharing them and avoid posting sensitive telemetry to public or third-party channels.

Risk: No-auth mode can expose snapshot data if used beyond a strictly local service.

Mitigation: Keep authentication enabled for network-accessible deployments and use no-auth mode only for local, trusted workflows.

## Reference(s):

- [Snapshot JSON Schema](references/json-schema.md)
- [Claw Insights Snapshot on ClawHub](https://clawhub.ai/lucal6/skills/claw-insights-snapshot)
- [Publisher Profile: lucal6](https://clawhub.ai/user/lucal6)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with REST API and CLI commands that produce PNG, SVG, or JSON snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports detail level, format, time range, theme, language, output path, token, port, quick mode, and dry-run options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
