## Description:

Save web content to Obsidian vault. Supports Twitter/X, WeChat MP, Xiaohongshu, YouTube, Bilibili, and any web page. Automatically routes to the best fetch method per platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Clipper to save supported social and web URLs into an Obsidian vault as Markdown files, with platform-specific routing for Twitter/X, WeChat MP, and general web pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically commit and push clipped content from the user's Obsidian vault.

Mitigation: Use it only with a vault and git remote where publishing clipped content is acceptable, and review clipped content before relying on automatic sync.

Risk: The skill fetches target URLs through external services or tools.

Mitigation: Avoid clipping sensitive URLs unless sharing them with the configured fetch services is acceptable.

Risk: The general web path depends on x-reader from a GitHub installation command.

Mitigation: Pin or review the x-reader dependency before installation.

Risk: The skill writes Markdown files into the detected Obsidian vault.

Mitigation: Confirm the selected vault path before use, especially when first evaluating the skill.

## Reference(s):

- [Clipper on ClawHub](https://clawhub.ai/pazzilivo/skills/clipper)
- [x-reader dependency](https://github.com/runesleo/x-reader.git)
- [Jina Reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with YAML frontmatter and JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves clips under an Obsidian vault and may return git_warnings when automatic git sync fails.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
