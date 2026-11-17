## Description:

Generates infographic image card series with 12 visual styles, 8 layouts, and 3 color palettes, breaking content into 1-10 cartoon-style image cards optimized for social media engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn source content into multi-card social media infographic series with selectable visual styles, layouts, palettes, prompts, and generation workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A prompt template may encourage image generators not to refuse sensitive or copyrighted-figure requests.

Mitigation: Review and revise the prompt-assembly wording so generated prompts respect the selected image backend's safety policies.

Risk: User-wide preference storage can unintentionally reuse watermark and style defaults across projects.

Mitigation: Use project-local preferences unless cross-project reuse is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-image-cards)
- [Publisher profile](https://clawhub.ai/user/jimliu)
- [Homepage from ClawHub metadata](https://github.com/JimLiu/baoyu-skills#baoyu-image-cards)
- [Prompt Assembly Guide](references/workflows/prompt-assembly.md)
- [Xiaohongshu Content Analysis Framework](references/workflows/analysis-framework.md)
- [Xiaohongshu Outline Template](references/workflows/outline-template.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Watermark Guide](references/config/watermark-guide.md)
- [Style Presets](references/style-presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance, image files]

**Output Format:** [Markdown workflow notes, Markdown prompt files, configuration guidance, and raster image outputs from the selected image backend]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt files before image generation, supports 1-10 card series, selectable styles/layouts/palettes, optional watermark preferences, and batch generation guidance.]

## Skill Version(s):

1.117.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
