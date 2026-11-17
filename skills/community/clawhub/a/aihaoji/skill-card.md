## Description:

Use when the user asks to search, read, export, manage, move, or auto-classify Ai好记 / AI好记 notes and notebooks, including 笔记本, 文件夹, 划线, 批注, 我的记录, 新建笔记本, 移动笔记, 移动笔记本, AI 自动归类整理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aihaoji-agent](https://clawhub.ai/user/aihaoji-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, read, export, organize, and move Ai好记 notes and notebooks through the Ai好记 open platform API. It supports authenticated note access and requires explicit confirmation before write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read note content and records, export notes, create or rename notebooks, delete notebooks, and move notes or notebooks through the Ai好记 API.

Mitigation: Use a least-privilege API key and require explicit user confirmation before write operations.

Risk: Stored API keys in ~/.aihaoji/config.json could expose account access if file permissions are too broad.

Mitigation: Protect ~/.aihaoji/config.json with user-only permissions or use environment variables instead.

Risk: The setup flow may invoke an unpinned npx command.

Mitigation: Verify the package name and version before running setup.

## Reference(s):

- [Server-resolved source repository](https://github.com/AiHaoJi-Agent/aihaoji-skills)
- [Ai好记 homepage](https://www.aihaoji.com)
- [Ai好记 Open Platform](https://openapi.aihaoji.com)
- [ClawHub skill listing](https://clawhub.ai/aihaoji-agent/skills/aihaoji)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with API request guidance, setup commands, and optional exported note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May access Ai好记 note content through authenticated API calls and may propose write operations only after user confirmation.]

## Skill Version(s):

0.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
