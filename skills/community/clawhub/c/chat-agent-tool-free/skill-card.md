## Description:

This skill provides a temporary password-protected real-time chat room with SSE streaming, a Web UI, and Agent CLI access for agent and human collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, and multi-agent teams use this skill to start a temporary chat room where agents and humans can join, send, listen to, and debug real-time collaboration messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for unrelated file, design, document-conversion, or generic automation tasks despite its chat-room purpose.

Mitigation: Configure routing so the skill is invoked only for temporary agent or human chat coordination.

Risk: Public tunnel mode can expose a room to anyone who receives or discovers the URL and password.

Mitigation: Use a strong unique password, share the URL only with trusted participants, avoid sensitive conversations, and stop the service when collaboration ends.

Risk: Messages are stored only in memory and are lost when the service stops or restarts.

Mitigation: Use the room for temporary coordination and preserve important decisions or outputs outside the chat before shutdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chat-agent-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chat server commands, room URLs, user-supplied passwords, and temporary Web UI or SSE access details.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
