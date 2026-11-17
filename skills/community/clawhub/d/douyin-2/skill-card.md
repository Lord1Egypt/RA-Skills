## Description:

抖音视频上传工具。支持登录抖音账号、上传视频、管理登录状态。当用户需要上传视频到抖音、登录抖音、检查抖音登录状态时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancelin111](https://clawhub.ai/user/lancelin111)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to log in to Douyin, upload videos with titles, descriptions, and tags, and manage locally stored login state for a Douyin account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Douyin session cookies and browser profile data locally.

Mitigation: Run it in a dedicated, low-privilege environment and avoid sharing the skill directory or generated cookie/profile files.

Risk: The skill can publish content to the connected Douyin account.

Mitigation: Use --no-publish when a draft is intended, and review account state and upload settings before using it with a sensitive account.

Risk: The security summary notes disabled browser sandboxing and broad browser permissions.

Mitigation: Review the browser permission and sandbox choices before deployment, especially for sensitive accounts or shared machines.

## Reference(s):

- [ClawHub Douyin Skill](https://clawhub.ai/lancelin111/skills/douyin-2)
- [Douyin MCP Server Homepage](https://github.com/lancelin111/douyin-mcp-server)
- [Douyin Creator Platform](https://creator.douyin.com)
- [Douyin](https://www.douyin.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation steps and local account-management guidance for Douyin upload workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
