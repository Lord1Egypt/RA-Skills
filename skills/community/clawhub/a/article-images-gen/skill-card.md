## Description:

Generates hand-drawn, minimalist illustrations for articles and can add the generated image references back into the article Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to generate hand-drawn article illustrations, prompt files, an outline, and Markdown image references for long-form content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article text may be sent to Gemini or Grok through browser automation.

Mitigation: Use the skill only with content approved for those services and avoid sensitive, confidential, or regulated article text unless an appropriate data-handling review has been completed.

Risk: The skill automatically edits article files after generating images.

Mitigation: Run it on trusted article paths, keep and review the generated backups, and inspect the Markdown diff before publishing.

Risk: Server security evidence reports unsafe shell command construction.

Mitigation: Prefer a fixed release that replaces shell interpolation with argument-array process execution before broad installation.

## Reference(s):

- [Project homepage](https://github.com/victor-skills/tree/main/skills/article-images-gen)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated PNG files, prompt Markdown files, an outline Markdown file, and edited article Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 16:9 image generation, writes outputs under /tmp/imageGen by default, and may insert image references into the source article.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
