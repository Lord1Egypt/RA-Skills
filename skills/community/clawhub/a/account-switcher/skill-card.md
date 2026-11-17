## Description:

通过 HTTP API 控制多账号矩阵管理工具，实现浏览器账号的启动、关闭及信息查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users managing browser account sessions use this skill to list accounts and start or stop a selected account by name or index through a local multi-account management application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Start and stop commands can affect active browser account sessions.

Mitigation: Use explicit account names or indexes and confirm the intended account before running start or stop commands.

Risk: The skill depends on a third-party local multi-account management application.

Mitigation: Install and run the skill only when the third-party application is trusted and its local server is intentionally enabled.

Risk: Python dependency installation can affect the user's environment.

Mitigation: Install Python dependencies such as requests in a virtual environment when possible.

## Reference(s):

- [账号切换器 ClawHub release](https://clawhub.ai/wociaozhongyunonghaole/skills/account-switcher)
- [Multi-account management tool website](https://zmt.scys6688.com/)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes command results to last_result.txt for UTF-8 result retrieval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
