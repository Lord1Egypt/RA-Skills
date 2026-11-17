## Description:

工程化备课系统（Course-Prep-Auto-Flow v1.0）将课程主题、受众画像和参考素材转化为分步确认的课程骨架、备课内容、配图规划和飞书文档输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, course designers, trainers, and content teams use this skill to prepare public classes, livestream courses, and workshops through a seven-step workflow from intake to final course documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-generation prompts and a Google API key may be sent to a configured third-party image endpoint.

Mitigation: Use restricted or disposable credentials, avoid sensitive teaching materials unless the data flow is approved, and require explicit confirmation before image generation or API sharing.

Risk: The workflow can create or share Feishu documents as final outputs.

Mitigation: Confirm document creation and sharing targets before execution, and review the generated course-prep and retrospective documents before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yipng05-max/skills/course-prep-afp)
- [Publisher profile](https://clawhub.ai/user/yipng05-max)
- [Detailed Feishu documentation](https://www.feishu.cn/docx/GmQUdwj4sosWxvxQp84cIf8NnQb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, staged prompts, inline shell commands, image prompts, and document URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-gated course-preparation artifacts; image generation and Feishu document creation require explicit user confirmation and configured credentials.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
