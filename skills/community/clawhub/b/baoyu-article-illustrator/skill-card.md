## Description:

Analyzes article structure, identifies positions requiring visual aids, generates illustrations with Type x Style x Palette three-dimension approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to analyze Markdown articles, choose appropriate visual placements, generate illustration prompts and raster images, and insert image links back into the article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes illustration assets and may edit article files.

Mitigation: Review generated prompts, image paths, and article changes before accepting them.

Risk: The codex-imagegen fallback can run an unpinned package from npm.

Mitigation: Use a pinned or trusted local Bun installation and avoid the npx -y bun fallback.

Risk: A bundled prompt line attempts to avoid refusals for sensitive or copyrighted figure requests.

Mitigation: Remove or revise that prompt line and follow the active image backend's safety and copyright policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-article-illustrator)
- [OpenClaw homepage](https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator)
- [Workflow](references/workflow.md)
- [Usage](references/usage.md)
- [Styles](references/styles.md)
- [Style Presets](references/style-presets.md)
- [Prompt Construction](references/prompt-construction.md)
- [Codex Imagegen](references/codex-imagegen.md)
- [Preferences Schema](references/config/preferences-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with saved prompt files, outline files, raster image assets, and Markdown image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before generation unless explicitly skipped; writes prompts before invoking an image backend.]

## Skill Version(s):

1.117.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
