## Description:

How to join, participate in, and leave group conversations on messaging platforms (WhatsApp, Signal, Telegram, etc.). Use when the owner tags the agent into a group chat, when the agent needs to open or close the participation gate, or as a reference for correct group chat behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanblanchfield](https://clawhub.ai/user/seanblanchfield)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to let an agent join owner-approved group chats, participate briefly, and leave cleanly after a timed or owner-requested close.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broaden group message delivery while active by opening groupAllowFrom to all senders.

Mitigation: Get explicit owner approval, limit activation to allowlisted groups, and restore the exact previous groupAllowFrom value when closing.

Risk: The skill can leave a group chat gate open longer than intended if the close job is missed or misconfigured.

Mitigation: Schedule a timed close, confirm the close time to the owner, and validate configuration changes before and after the active window.

Risk: The troubleshooting guidance can erase session history if transcript clearing is used carelessly.

Mitigation: Prefer a supported reset flow or back up the session transcript before clearing it.

## Reference(s):

- [Chat Group Behavior ClawHub skill page](https://clawhub.ai/seanblanchfield/skills/chat-group-behavior)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline configuration paths and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
