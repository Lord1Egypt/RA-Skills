## Description:

Generates professional infographics by analyzing source content, recommending layout and style combinations, and producing publication-ready visual outputs across 21 layout types and 20 visual styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn source material into structured infographic content, select an appropriate visual layout and style, generate an image prompt, and produce a finished infographic asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted source documents or a project-local EXTEND.md can influence the generated infographic workflow.

Mitigation: Use the skill in trusted repositories when possible and review source content, EXTEND.md preferences, generated prompts, and generated images before publishing.

Risk: Generated prompts or images may be inaccurate, misleading, or unsuitable for the intended audience.

Mitigation: Compare analysis.md, structured-content.md, prompts/infographic.md, and infographic.png against the original source before using the output externally.

Risk: Source content may include credentials, secrets, or sensitive material that should not appear in generated outputs.

Mitigation: Follow the artifact workflow requirement to strip credentials, API keys, tokens, and secrets before including source material in outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nengnengz/skills/baoyu-infographic-2)
- [OpenClaw Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)
- [Analysis Framework](references/analysis-framework.md)
- [Structured Content Template](references/structured-content-template.md)
- [Base Prompt Template](references/base-prompt.md)
- [Layout Definitions](references/layouts/)
- [Style Definitions](references/styles/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands, image]

**Output Format:** [Markdown analysis and structured content files, an image-generation prompt, and a PNG infographic output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an infographic output directory containing source content, analysis, structured content, prompts, and infographic.png.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter version 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
