## Description:

帮助中文长篇小说创作者用可读文件维护人物、世界观、大纲和章节，并由当前 AI 阅读相关资料进行连续性审读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向中文小说作者及协作 Agent，用于整理长篇作品设定、人物、卷纲、时间线和章节，并在读取相关正文后审查连续性。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuity feedback may be incomplete when the AI has not read the relevant story materials.

Mitigation: Read the related character notes, settings, outline, timeline, and chapters; cite file and line or chapter anchors, and mark insufficient context as needs_review.

## Reference(s):

- [连续性检查清单](references/continuity-check.md)
- [ClawHub 发布页](https://clawhub.ai/xxjrq/skills/fiction-crafter-cn)

## Skill Output:

**Output Type(s):** [Markdown files, JSON, Shell commands, Writing guidance]

**Output Format:** [Markdown project files, a JSON structure-check report, and setup/check commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper checks required paths and non-empty files; continuity analysis is performed by the current AI after reading relevant story materials.]

## Skill Version(s):

1.0.2 (source: frontmatter metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
