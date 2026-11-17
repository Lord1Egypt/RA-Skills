## Description:

Mission Control is a CLI-first system health aggregator for autonomous AI agents that checks agent processes, resources, cron jobs, services, and OpenClaw status in one report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhawala4](https://clawhub.ai/user/dhawala4)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators running autonomous AI infrastructure use this skill to check system health, inspect agent and service status, review resource usage, and gather operational signals before deployments or during incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local process, port, cron, service, resource, and recent journal information to the agent.

Mitigation: Install only in trusted environments where that host inspection is acceptable, and restrict use to trusted operators.

Risk: The restart command can perform sudo-backed systemd service restarts without strong built-in service limits.

Mitigation: Require explicit user confirmation before restart use, prefer OpenClaw-specific service names, and review sudo policy before enabling the skill.

## Reference(s):

- [Mission Control on ClawHub](https://clawhub.ai/dhawala4/skills/dhawala-mission-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text or JSON, with agent-facing summaries in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only status checks by default; service restart requires explicit confirmation and sudo.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
