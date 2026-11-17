## Description:

为出海品牌制定极简视觉识别方案，涵盖品牌定位、色彩与留白、线条图形、表情符号及应用物料提示词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzfly](https://clawhub.ai/user/yzfly)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

品牌负责人、创业团队和设计人员可用它为面向国际市场的品牌建立统一视觉方向，并生成适用于网站、社交媒体和周边物料的设计规范与提示词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance uses changing remote sources, installs globally, and skips confirmation.

Mitigation: Review the command, inspect a fixed revision, and install only the intended skill.

Risk: Brand details may be sent to the configured image provider when generating images.

Mitigation: Avoid including confidential brand information unless the provider is approved to receive it.

Risk: The stated CC BY-NC 4.0 license restricts commercial use of the skill.

Mitigation: Confirm the applicable rights and obtain permission before commercial use.

## Reference(s):

- [Brand specification template](artifact/references/brand-spec-template.md)
- [Application prompt templates](artifact/references/application-prompts.md)
- [Anti-cheapness checklist](artifact/references/anti-cheap-checklist.md)
- [ClawHub release page](https://clawhub.ai/yzfly/skills/breathing-brand)
- [hallmark](https://github.com/Nutlope/hallmark)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown brand specification and social copy with reusable image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include brand rules, application prompts, and a website layout description; generated images depend on host capabilities.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
