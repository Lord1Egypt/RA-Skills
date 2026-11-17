## Description:

为文章规划并生成可读性强的极简强线条手绘配图。先建立文章地图，识别段落适合流程图、架构图、对比图、关系图、结构图还是概念插图，再通过构思卡组织单一命题、原文指纹、信息单位、阅读顺序和固定橙白圆猫角色。构思通过可读性测试后默认直接生成。用户说配图、手绘配图、给文章配图、文章插图、技术文章插图、流程图、架构图、关系图或 illustrate my article 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and content teams use this skill to analyze Chinese-oriented articles, choose where illustrations help comprehension, and generate minimalist hand-drawn article visuals with clear insertion guidance and reusable prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article text can include sensitive or private material that may be incorporated into ImageGen prompts or prompt archives.

Mitigation: Review and redact sensitive article content and prompts before image generation or local archiving.

Risk: Generated illustrations may contain incorrect Chinese labels, unwanted text, or visual artifacts.

Mitigation: Inspect generated images before use and regenerate or revise prompts when labels, layout, or article-specific details are wrong.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/article-metaphor-illustrator)
- [配图构思协议](artifact/references/conception-protocol.md)
- [常用图型识别与绘制规范](artifact/references/diagram-types.md)
- [提示词模板](artifact/references/prompt-templates.md)
- [视觉转译指南](artifact/references/visual-translation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image generation prompts, Files, Guidance]

**Output Format:** [Markdown guidance with generated image files when ImageGen is available, plus archived bilingual prompts and insertion notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article body content may be transformed into ImageGen prompts; successful runs can save generated images and prompt archives locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
