## Description:

Search markdown knowledge bases efficiently using qmd. Use this when searching Obsidian vaults or markdown collections to find relevant content with minimal token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshumanbh](https://clawhub.ai/user/anshumanbh)

### License/Terms of Use:


## Use Case:

Developers, engineers, and knowledge workers use this skill to search local Markdown collections such as Obsidian vaults with qmd and receive concise snippets with file paths instead of reading full files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qmd from a remote repository may execute or install code the user has not reviewed.

Mitigation: Review the qmd repository or pin a trusted version before installation, and avoid elevated privileges during install.

Risk: Adding a local collection indexes Markdown content that may contain private or sensitive notes.

Mitigation: Only add collections the user is comfortable indexing and searching through qmd.

Risk: Search results may omit relevant information when the wrong search mode or stale embeddings are used.

Mitigation: Use BM25 for exact terms, vector search for conceptual queries, and refresh embeddings after significant content changes.

## Reference(s):

- [QMD GitHub Repository](https://github.com/tobi/qmd)
- [QMD Search ClawHub Skill Page](https://clawhub.ai/anshumanbh/skills/anshumanbh-qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and concise search-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output depends on locally installed qmd collections and may include file paths, snippets, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
