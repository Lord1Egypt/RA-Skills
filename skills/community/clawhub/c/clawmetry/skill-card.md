## Description:

Real-time observability for OpenClaw agents with a local dashboard and optional encrypted cloud sync for costs, tokens, sessions, tool calls, memory, crons, and system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivekchand](https://clawhub.ai/user/vivekchand)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw agent activity, usage cost, token consumption, sessions, tool calls, memory files, scheduled jobs, alerts, approvals, and system health from a local dashboard or optional cloud sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects or exposes sensitive observability data including conversations, memory files, tool inputs and results, logs, channel metadata, token usage, and costs.

Mitigation: Install only when that collection is acceptable, treat dashboard access as sensitive, and avoid exposing local endpoints to untrusted users.

Risk: Optional cloud sync sends encrypted telemetry to an external service using API-key based access.

Mitigation: Enable cloud sync only after trusting the external binary and service, protect CLAWMETRY_API_KEY, and review whether encrypted remote telemetry fits the deployment policy.

## Reference(s):

- [ClawMetry ClawHub skill page](https://clawhub.ai/vivekchand/skills/clawmetry)
- [Publisher profile](https://clawhub.ai/user/vivekchand)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline commands and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to local dashboard URLs, local API endpoints, or ClawMetry setup commands when observability context is relevant.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
