## Description:

Enable communication, coordination, and information exchange between OpenClaw agents through controlled multi-agent chat sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saullockyip](https://clawhub.ai/user/saullockyip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to create, list, view, and delete A2A sessions and to format messages for coordination with other OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages sent through this skill are shared with another agent context.

Mitigation: Avoid including secrets or unnecessary private data in A2A messages.

Risk: Session metadata is stored locally until deleted.

Mitigation: Delete sessions that are no longer needed and review local session records according to the workspace's retention expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saullockyip/skills/a2a-chatting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces session-management commands and required sessions_send message formats; messaging is performed through the agent's sessions_send tool.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
