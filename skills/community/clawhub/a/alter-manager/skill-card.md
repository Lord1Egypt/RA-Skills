## Description:

Alter Manager helps an agent create, list, delete, and route messages to independent OpenClaw sub-sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnluicn](https://clawhub.ai/user/johnluicn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage multiple OpenClaw sub-sessions for separate work streams, including creating labeled sessions, listing active sessions, routing messages, and deleting selected sessions after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw session metadata and persist a routing target in the workspace.

Mitigation: Review the active session list and routing state before forwarding sensitive work to a sub-session.

Risk: The skill can delete selected sessions after confirmation while archiving transcripts.

Mitigation: Confirm the target label and session key before deletion, and rely on archived transcripts when recovery is needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session labels, session keys, routing state details, and deletion results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
