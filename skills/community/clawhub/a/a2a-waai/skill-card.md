## Description:

A2A helps agents discover and invoke peer agents through a compact Python client, server, registry, and message model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents over WebSocket endpoints, delegate work to specialized agents, and build multi-agent workflows with call, notification, and asynchronous task message types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Networked agent calls are exposed without clear authentication or transport security.

Mitigation: Use endpoint allowlisting, authenticated peers, encrypted transport, and trusted networks before using the skill for real agents.

Risk: Outbound delegation can share sensitive data or trigger consequential tasks through another agent.

Mitigation: Do not send secrets, private user data, or credentials through peer calls, and require explicit user approval for consequential delegation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaibuer/skills/a2a-waai)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; the Python module imports websockets when client connections are used.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
