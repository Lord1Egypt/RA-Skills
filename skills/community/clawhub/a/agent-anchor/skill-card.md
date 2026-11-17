## Description:

Agent Anchor helps OpenClaw users run a local dashboard that snapshots agent state, tracks tasks, monitors cron jobs, and supports recovery after interruptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metariot2026](https://clawhub.ai/user/metariot2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up a browser-based dashboard for agent state recovery, task tracking, activity review, and scheduled-job monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted agent state may contain secrets, private personal data, or sensitive operational context.

Mitigation: Keep state files free of secrets and private personal data, restrict file permissions, and review snapshots before sharing or backing them up.

Risk: The local dashboard is described as an unauthenticated web server on port 3456.

Mitigation: Bind the dashboard to localhost only and do not expose port 3456 on public or shared networks.

## Reference(s):

- [Agent Anchor on ClawHub](https://clawhub.ai/metariot2026/skills/agent-anchor)
- [MetaRiot2026 Publisher Profile](https://clawhub.ai/user/metariot2026)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operation guidance for a local OpenClaw dashboard; no structured machine-readable output is specified.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
