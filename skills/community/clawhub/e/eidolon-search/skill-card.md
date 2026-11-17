## Description:

Eidolon Search helps agents build and query a local SQLite FTS5 index over Markdown memory files to retrieve relevant snippets with lower context usage than reading full files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dev-jslee](https://clawhub.ai/user/dev-jslee)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when an agent needs to search across Markdown memory files, daily notes, or local knowledge corpora without loading full files into context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local index copies Markdown file contents into a SQLite database, which can retain sensitive material if broad or unintended directories are indexed.

Mitigation: Index only directories intentionally selected for agent memory search and store the database where its contents are appropriate for the workspace.

Risk: The optional cache benchmark may request sudo and attempt a host-wide OS cache reset.

Mitigation: Avoid running scripts/benchmark-cache.py on shared, production, or sensitive machines unless the operator understands the host-wide cache effect.

Risk: FTS5 keyword search can miss relevant information when queries contain typos, synonyms, semantic paraphrases, or complex conditions.

Mitigation: Use specific terms, phrase queries, synonym expansion, and follow-up full-file reads for important results or empty searches.

## Reference(s):

- [Performance](references/PERFORMANCE.md)
- [Search Quality Limitations and Improvement Direction](references/QUALITY.md)
- [ClawHub Skill Page](https://clawhub.ai/dev-jslee/skills/eidolon-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text search snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes matching file paths, snippets, and relevance ranks from a local SQLite database.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
