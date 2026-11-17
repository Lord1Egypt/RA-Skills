## Description:

Provides real-time monitoring, log search, service status, alerts, and configuration restore guidance for OpenClaw Gateway and related services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yes999zc](https://clawhub.ai/user/yes999zc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or operate a local monitoring dashboard for OpenClaw Gateway, inspect logs and service status, manage LiteLLM and oMLX-related checks, and restore configuration from backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release tells users to run and optionally persist unreviewed code fetched from a mutable GitHub repository.

Mitigation: Review carefully before installing; prefer a release that packages server.js, the LaunchAgent plist, and all runtime files in the skill artifact, or pins and verifies a specific commit.

Risk: The dashboard is a local service with authority to read logs and control Gateway, LiteLLM, and related operations.

Mitigation: Inspect exactly what the service runs before enabling the LaunchAgent, and avoid enabling persistence until the local service behavior and access are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yes999zc/skills/gateway-monitor)
- [Gateway Monitor repository referenced by artifact](https://github.com/yes999zc/gateway-monitor)
- [Dashboard screenshot referenced by artifact](https://raw.githubusercontent.com/yes999zc/gateway-monitor/main/screenshots/dashboard.png)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, environment variables, endpoint lists, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local service control and configuration restore steps that should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: evidence.json release.version and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
