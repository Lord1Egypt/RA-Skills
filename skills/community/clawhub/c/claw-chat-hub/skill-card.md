## Description:

Real-time agent communication module supporting provider and consumer bidirectional messaging, channel management, and message history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangboheng](https://clawhub.ai/user/tangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add WebSocket-based real-time chat between provider and consumer agents, including chat requests, accept or reject flows, message sending, session ending, and history retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent messages and history are sent through a WebSocket Hub endpoint.

Mitigation: Use only trusted Hub endpoints, prefer WSS, and avoid sending secrets or sensitive personal data through the channel.

Risk: The api_key parameter may be misleading if the client and Hub do not enforce authentication.

Mitigation: Do not rely on api_key for authentication unless the client and Hub are verified to enforce it.

Risk: The security verdict is suspicious for production or shared environments.

Mitigation: Review and scan the skill before installation or deployment.

## Reference(s):

- [Claw Chat Hub on ClawHub](https://clawhub.ai/tangboheng/skills/claw-chat-hub)
- [Publisher profile: tangboheng](https://clawhub.ai/user/tangboheng)

## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown documentation with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a HUB_URL-compatible WebSocket Hub endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
