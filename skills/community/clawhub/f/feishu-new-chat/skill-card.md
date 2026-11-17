## Description:

Create a new topic in a Feishu topic-group, and optionally add the first in-thread reply with an optional @mention by sending as the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxxbb](https://clawhub.ai/user/dxxbb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to start a clean Feishu topic-group conversation, optionally seed the first in-thread reply, and carry concise prior context into a new topic when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-requested Feishu topic messages and replies as the user.

Mitigation: Require an explicit user request before sending and stop if user-auth Feishu messaging is unavailable or expired.

Risk: When carrying prior context into a new topic, a short summary of that context may be posted into the selected Feishu group.

Mitigation: Carry over only the minimum relevant context and put it in the topic-opening message only when the user asks for context transfer.

Risk: If the destination is not a Feishu topic-group, the send may create a normal group message rather than a topic.

Mitigation: Resolve the destination group first and explain the limitation or ask for a valid Feishu topic-group when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxxbb/skills/feishu-new-chat)
- [Publisher profile](https://clawhub.ai/user/dxxbb)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown and Feishu text message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a top-level Feishu topic message and, when requested, one in-thread reply with optional Feishu @mention markup.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
