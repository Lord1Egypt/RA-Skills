## Description:

Converts Markdown to styled HTML with WeChat-compatible themes, including code highlighting, math, Mermaid PNG rendering through headless Chrome, PlantUML, footnotes, alerts, infographics, and optional bottom citations for external links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content authors, and agents use this skill to convert Markdown files into styled HTML suitable for WeChat Official Account and similar publishing workflows. It is useful when the user needs themed HTML output, Mermaid or PlantUML rendering, image handling, or optional bottom citations for external links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download or invoke a Bun runtime at use time through the npx fallback.

Mitigation: Prefer a preinstalled, trusted Bun runtime and review the runtime path before installation or execution.

Risk: Markdown containing remote image URLs can cause the user's machine to fetch external resources during conversion.

Mitigation: Convert only trusted Markdown, or remove and review remote image URLs before running the skill.

Risk: The conversion writes HTML output, creates backups, and may create Mermaid cache files beside the input.

Mitigation: Run the skill with limited filesystem access and inspect output paths before using it on important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-markdown-to-html)
- [Metadata homepage](https://github.com/JimLiu/baoyu-skills#baoyu-markdown-to-html)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON]

**Output Format:** [Markdown guidance with shell command examples; generated HTML files and JSON conversion results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an HTML file beside the input Markdown file, may create timestamped backups for existing HTML files, and may cache Mermaid PNG files under imgs/.mermaid-cache.]

## Skill Version(s):

1.117.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
