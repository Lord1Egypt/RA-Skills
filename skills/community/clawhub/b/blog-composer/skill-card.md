## Description:

Jekyll blog authoring UI for managing posts, drafts, tags, and publishing workflows for static sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and site maintainers use this skill to create, edit, preview, organize, and publish Markdown posts for Jekyll or static-site blogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file and publish actions can modify blog content or push changes without enough containment.

Mitigation: Bind services only to localhost, require authentication for any web API, and add clear confirmation before publish or delete actions.

Risk: Post filenames and metadata can affect filesystem writes under the configured blog directory.

Mitigation: Validate filenames with a strict allowlist, resolve paths under the expected posts directory, and reject path traversal or unexpected extensions.

Risk: Rendered Markdown and metadata may include unsafe or misleading content before publication.

Mitigation: Sanitize rendered Markdown and front matter, and require human review before saving or publishing generated content.

Risk: AI-assisted generation and research features may send prompts or source material to external providers.

Mitigation: Disclose provider use and data sharing, make AI generation opt-in, and avoid sending secrets or unpublished sensitive content.

Risk: Hardcoded local paths and secret-file paths can fail outside the publisher environment and may expose operational assumptions.

Mitigation: Move blog roots and API-key locations into user-controlled configuration and document required permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/blog-composer)
- [Publisher Profile](https://clawhub.ai/user/amrree)
- [TheSolAI Blog](https://thesolai.github.io)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown blog content, Jekyll front matter, configuration notes, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local blog post files and trigger git-based publish actions when run.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
