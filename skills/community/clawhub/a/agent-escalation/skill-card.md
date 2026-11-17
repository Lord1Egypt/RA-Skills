## Description:

Escalates an agent's unresolved issue to a configured supervisor through a webhook gateway after several failed attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superworldsavior](https://clawhub.ai/user/superworldsavior)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to escalate unresolved technical, scope, or ambiguity issues to a configured supervisor with a concise problem statement, attempted fixes, and current result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escalation arguments may include sensitive troubleshooting context that is forwarded to a supervisor and delivery channel.

Mitigation: Redact passwords, API keys, tokens, personal data, and raw customer logs before invoking the skill.

Risk: The webhook uses a bearer token and should only target trusted infrastructure.

Mitigation: Verify the gateway host, port, and token before use; keep the gateway on loopback or require TLS for any non-local destination.

Risk: Default supervisor, channel, and recipient settings can send escalations to the wrong destination if not reviewed.

Mitigation: Configure and confirm the supervisor agent, delivery channel, and recipient for the installing organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superworldsavior/skills/agent-escalation)
- [Publisher profile](https://clawhub.ai/user/superworldsavior)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted escalation message and shell command status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured webhook gateway, bearer token, supervisor agent, delivery channel, and recipient.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
