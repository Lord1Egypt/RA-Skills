## Description:

Generates professional slide deck images from content by creating outlines with style instructions and then generating individual slide images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn source content into shareable, self-explanatory slide decks. It guides outline creation, image prompt generation, raster slide generation, and optional PPTX or PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety-bypass prompt text may steer image generation toward refusing fewer requests than expected.

Mitigation: Review and remove the anti-refusal wording in references/base-prompt.md before operational use.

Risk: Executable fallback paths can run unpinned or unreviewed local tooling.

Mitigation: Use a reviewed bun installation, avoid npx -y bun unless pinned and trusted, and do not set BAOYU_CODEX_IMAGEGEN_BIN to an unreviewed executable.

Risk: Generated prompts may be embedded in PPTX speaker notes and disclosed when decks are shared.

Mitigation: Inspect exported PPTX files and remove speaker notes before sharing decks that include sensitive prompts or source material.

Risk: External image-generation backends may receive slide content or reference material.

Mitigation: Use only approved image-generation backends and avoid sending confidential content to unapproved services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-slide-deck)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-slide-deck)
- [Analysis framework](references/analysis-framework.md)
- [Design guidelines](references/design-guidelines.md)
- [Content rules](references/content-rules.md)
- [Codex image generation notes](references/codex-imagegen.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, images, presentation files]

**Output Format:** [Markdown outlines and prompts, PNG or JPEG slide images, and optional PPTX or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 16:9 slide images and may embed generated prompts in PPTX speaker notes when prompt files are present.]

## Skill Version(s):

1.117.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
