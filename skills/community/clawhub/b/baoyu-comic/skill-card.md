## Description:

Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and batch-capable image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Baoyu Comic to turn educational, biographical, tutorial, or concept content into original knowledge comics with storyboards, character references, page prompts, generated raster images, and merged PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback paths can download or execute local tooling during normal use.

Mitigation: Install trusted Bun tooling directly, avoid the npx -y bun fallback, and review generated commands before execution.

Risk: Comic prompts and reference images may be sent to image-generation backends.

Mitigation: Use approved image-generation backends and avoid submitting sensitive source material or reference images.

Risk: Default presets may include third-party character or style assumptions.

Mitigation: Review selected presets, character plans, and prompt files before image generation.

## Reference(s):

- [Baoyu Comic Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-comic)
- [Complete Workflow](references/workflow.md)
- [Comic Content Analysis Framework](references/analysis-framework.md)
- [Auto Selection](references/auto-selection.md)
- [Base Prompt](references/base-prompt.md)
- [Storyboard Template](references/storyboard-template.md)
- [Character Definition Template](references/character-template.md)
- [Partial Workflows](references/partial-workflows.md)
- [Codex Imagegen Wrapper Invocation](references/codex-imagegen.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Watermark Guide](references/config/watermark-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, prompt files, raster images, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an available raster image-generation backend and local Bun-compatible tooling for PDF merge operations.]

## Skill Version(s):

1.117.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
