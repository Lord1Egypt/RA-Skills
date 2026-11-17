## Description:

Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, creators, and developers use this skill to turn source material into educational comics with analysis, storyboards, character references, image prompts, generated page images, and a merged PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal execution may use an unpinned downloaded Bun runtime through npx.

Mitigation: Review runtime behavior before installing; prefer a trusted local Bun installation or ask the publisher to pin the npx fallback and dependencies.

Risk: The ohmsha preset can generate Doraemon-derived characters by default.

Mitigation: Review generated character prompts and replace derivative defaults when originality or rights clearance is required.

Risk: User-scope preferences can store EXTEND.md under the user's home directory for future projects.

Mitigation: Choose project-scope preferences or review the user-scope EXTEND.md before reuse across projects.

## Reference(s):

- [Baoyu Comic ClawHub page](https://clawhub.ai/nengnengz/skills/baoyu-comic-2)
- [Baoyu Skills homepage](https://github.com/JimLiu/baoyu-skills#baoyu-comic)
- [Complete Workflow](references/workflow.md)
- [Partial Workflows](references/partial-workflows.md)
- [Auto Selection](references/auto-selection.md)
- [Preferences Schema](references/config/preferences-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, image-generation prompts, generated image files, PDF output, and shell commands for PDF merging]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized under comic/{topic-slug}/ with analysis, storyboard, character references, prompts, page images, and a merged PDF.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; source skill frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
