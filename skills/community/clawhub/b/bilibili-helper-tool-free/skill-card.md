## Description:

B站创作助手免费版为个人UP主生成B站视频标题、简介模板和标签推荐，帮助快速准备投稿内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to draft Bilibili video titles, descriptions, and tag sets in Chinese for normal content-publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file-writing authority even though its stated purpose is pure text generation.

Mitigation: Install only after reviewing the permissions, and prefer a package revision that removes exec/write or documents a narrow command and file-writing scope.

Risk: The documentation is inconsistent about whether command execution or file output is required.

Mitigation: Before deployment, confirm expected behavior in a sandbox and restrict the agent to text-only output unless a specific reviewed command is needed.

Risk: Generated titles, descriptions, and tags may be misleading, low quality, or misaligned with platform expectations.

Mitigation: Have the creator review and edit generated content before publishing it to Bilibili.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thcjp/skills/bilibili-helper-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language content-generation output based on the user's supplied video topic.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
