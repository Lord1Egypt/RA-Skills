## Description:

撤回飞书群消息。以用户身份撤回（recall）飞书群聊或单聊中的消息，支持单条撤回、批量撤回和按时间范围撤回。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tz826](https://clawhub.ai/user/tz826)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace operators and agents use this skill to recall Feishu group or direct messages by message ID, quoted-message context, batch selection, or time window. It is intended for authorized users, group owners, or administrators who need controlled message removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete Feishu messages in bulk without built-in preview or confirmation safeguards.

Mitigation: Require the agent or operator to confirm the target chat, message IDs or time window, and message count before any batch deletion.

Risk: Group owners or administrators may be able to recall messages from other members.

Mitigation: Use only in workspaces where message recall is intended and limit use to authorized operators with an explicit deletion request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tz826/skills/feishu-recall-message)
- [Publisher profile](https://clawhub.ai/user/tz826)

## Skill Output:

**Output Type(s):** [guidance, API Calls, shell commands]

**Output Format:** [Markdown with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational constraints, batch-recall steps, pagination notes, and result reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
