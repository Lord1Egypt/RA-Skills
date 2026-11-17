## Description:

Automates Douyin Creator Center publishing and account operations, with Feishu-mediated login checks, content planning, data reporting, comment and direct-message replies, and digital-human marketing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrchenyh](https://clawhub.ai/user/mrchenyh)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, OpenClaw users, and developers use this skill to publish Douyin video or image-text content, coordinate login and verification through Feishu, sync Douyin data to Feishu Bitable, and generate follow-up marketing content. It is also used to route customer Feishu messages into guarded automation for publishing, reporting, auto-replies, and digital-human video workflows.

### Deployment Geography for Use:

Global, subject to Douyin, Feishu, and local platform availability and compliance requirements.

## Known Risks and Mitigations:

Risk: The scanner verdict is suspicious because the skill installs persistent local automation and scheduling.

Mitigation: Install only on a dedicated machine or OpenClaw profile, review the bootstrap script before running --apply, and monitor or disable the supervisor and scheduler when automation is not intended.

Risk: The scanner summary reports broad session-log access and fallback inference for Feishu routing.

Mitigation: Pass explicit Feishu messageId and chatId, restrict who can call the MCP tools, and avoid relying on session-log inference for sensitive workflows.

Risk: The scanner summary reports unrestricted URL fetching.

Mitigation: Accept media and cover URLs only from trusted sources, validate fieldized publish tasks before execution, and keep human review in place before publishing.

Risk: The scanner summary reports agent-response steering in an automation flow that can publish content and message customers.

Mitigation: Require human confirmation for publishing, login, SMS verification, and security-verification steps, and keep customer-facing messages concise and reviewable.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/mrchenyh/skills/douyin-upload-mcp-skill)
- [English README](README.en.md)
- [Customer Install Guide](references/customer-install-guide.md)
- [Login And Feishu Flow](references/login-feishu.md)
- [Data, Comments, And DMs](references/data-interactions.md)
- [Publish Flow](references/publish-flow.md)
- [Publish Task Contract](references/publish-task.md)
- [Local Configuration Template](references/skill-local-config.md)
- [XiaoIce Service Configuration](references/xiaoice-service-config.md)
- [Operational Pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell commands, and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include operational status, customer-facing Feishu copy, task JSON, publishing plans, reports, screenshots, and local configuration guidance; execution depends on configured credentials, browser state, Douyin and Feishu access, and provider APIs.]

## Skill Version(s):

0.1.8 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
