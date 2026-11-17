## Description:

Generates Chinese motherhood praise-card content from a user's parenting experience, including empathetic praise text, Gemini image prompts, and publishing copy for Xiaohongshu, Douyin, and Kuaishou.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn real parenting moments into share-ready Chinese praise cards, image-generation prompts, and platform-specific social copy. The skill is intended for motherhood and childcare contexts and gates passive emotional triggers and local file saving behind user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated posts may include private parenting, family, or emotional details that the user does not want to share publicly.

Mitigation: Review generated text and prompts before posting, and remove or rewrite any private family details.

Risk: Generated files may persist sensitive content on local disk.

Mitigation: Save files only after explicit confirmation and only when the displayed path is the expected ./assets/output/ location.

## Reference(s):

- [Skill README](README.md)
- [情绪识别器](references/01-情绪识别器/SKILL.md)
- [文生图提示词写手](references/02-文生图提示词写手/SKILL.md)
- [风格适配器](references/03-风格适配器/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/skills/caihongpi-mother)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown text with Gemini image prompts, praise-card copy, platform posting guidance, and optional local files after confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Prompt .txt and README.md files under ./assets/output/ only after explicit user confirmation.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
