## Description:

Agent Expression helps chat agents search local meme and sticker packs by mood using vector and full-text retrieval, ingest images with optional vision captioning, and return real absolute image paths for supported hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyh-001](https://clawhub.ai/user/yyh-001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to add local meme and sticker search, preview, delivery, and image ingestion to chat agents across Cursor, Codex, Claude Code, Hermes, and custom bots while avoiding invented image paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can pull mutable remote code and link or update skill directories across multiple agent hosts.

Mitigation: Avoid one-line remote execution; download and inspect the installer, then install from a verified commit or release.

Risk: Vision captioning and embedding workflows may send image content, captions, or related text to the configured API provider.

Mitigation: Use these features only with images suitable for the configured provider and avoid processing sensitive local content.

Risk: Running ingestion from projects with sensitive environment files may expose configuration or secrets through local workflows.

Mitigation: Run ingestion from a clean working directory and keep API keys in the configured environment files rather than source code.

Risk: The bundled meme pack uses third-party media with separate rights from the skill code.

Mitigation: Review the bundled pack credits and upstream license before reuse, especially for commercial or redistributed media packs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yyh-001/skills/agent-expression)
- [Host Adaptation Guide](references/hosts.md)
- [Meme Database Schema](references/meme-db-schema.md)
- [Meme Embeddings Schema](references/meme-embeddings-schema.md)
- [Meme Category Reference](references/categories.md)
- [Bundled Pack Credits](packs/official-001/CREDITS.md)
- [Upstream Meme Pack Source](https://github.com/anka-afk/astrbot-meme-pack-official-01)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and absolute local image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful meme search emits one real absolute image path; Hermes delivery may use a MEDIA:/path line.]

## Skill Version(s):

2.1.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
