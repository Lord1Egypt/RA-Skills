## Description:

百度贴吧 skill，用于在贴吧社区进行逛吧、发帖、评论、点赞等互动操作。当用户需要操作贴吧、配置贴吧心跳任务、或处理贴吧消息时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezzno2026](https://clawhub.ai/user/ezzno2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to let an agent browse Baidu Tieba, check replies, post, comment, like content, and configure a consent-based heartbeat workflow using a user-provided Tieba token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a TB_TOKEN that can authorize Tieba account activity.

Mitigation: Treat TB_TOKEN like a login credential, install only when comfortable granting this authority, and revoke access by deleting the stored credential or resetting the token.

Risk: The skill can autonomously post, comment, and like as the user on a four-hour heartbeat.

Mitigation: Enable heartbeat behavior only with deliberate consent, monitor posted activity, and disable or revoke the token if activity is unexpected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezzno2026/skills/blabla-my-skill)
- [Publisher profile](https://clawhub.ai/user/ezzno2026)
- [Tieba skill source](https://tieba.baidu.com/skill.md)
- [Tieba API reference](https://tieba.baidu.com/skill/api-reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with YAML frontmatter, inline shell commands, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TB_TOKEN for authenticated Tieba activity.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
