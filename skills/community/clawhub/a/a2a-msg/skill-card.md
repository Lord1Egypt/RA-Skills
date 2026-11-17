## Description:

Communicates with other OpenClaw instances through a Redis message queue using a user-provided Redis server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaodaabao](https://clawhub.ai/user/gaodaabao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send, receive, inspect, and optionally auto-process messages between agent instances through Redis queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto mode can process queued Redis messages as commands and send automatic replies without strong sender authentication.

Mitigation: Use auto mode only with trusted peers and avoid scheduling it until sender authentication and per-command authorization are in place.

Risk: Messages and credentials depend on a user-operated Redis deployment that may lack secure transport or network restrictions.

Mitigation: Keep Redis off the public internet, use ACLs and a strong password, and prefer TLS or a private tunnel.

Risk: Auto-processing may disclose local skill names or process sensitive message content.

Mitigation: Do not use the skill with sensitive messages unless disclosure has been reviewed and access controls are configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaodaabao/skills/a2a-msg)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Redis connection settings through A2A_REDIS_HOST, A2A_REDIS_PORT, A2A_REDIS_PASSWORD, A2A_MY_ID, and A2A_PEER_ID.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
