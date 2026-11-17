## Description:

Chat Bus lets users and agents exchange direct, room, broadcast, and history messages through JSON files in a shared filesystem directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to set up lightweight file-based messaging over a trusted shared directory for direct messages, rooms, broadcasts, and message history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callers can claim other users because the released skill does not authenticate callers.

Mitigation: Install only where all participants already trust each other and have equivalent access until caller authentication is added.

Risk: Unvalidated path components can read, write, or delete outside the intended chat namespace.

Mitigation: Constrain all operations to a trusted chat root and validate path components before using the skill for private or adversarial multi-user chat.

Risk: Messages are stored as plaintext files in the shared directory.

Mitigation: Avoid sensitive content unless directory access controls and any required encryption are handled outside the skill.

## Reference(s):

- [chat-bus protocol reference](references/protocol.md)
- [Chat Bus ClawHub release page](https://clawhub.ai/wangjiaocheng/skills/chat-bus)
- [wangjiaocheng publisher profile](https://clawhub.ai/user/wangjiaocheng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON command examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces filesystem-backed JSON chat messages and status responses when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
