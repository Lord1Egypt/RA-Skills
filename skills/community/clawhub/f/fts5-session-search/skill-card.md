## Description:

Full-text search across all OpenClaw session logs using SQLite FTS5, with keyword search, topic queries, time-range filtering, and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larios613-hub](https://clawhub.ai/user/larios613-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and query a local SQLite FTS5 index of OpenClaw session logs so they can retrieve prior conversations by keyword, topic, time range, or session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index sensitive OpenClaw session logs into a searchable local database.

Mitigation: Use it only for sessions appropriate for local indexing, restrict SEARCH_AGENTS to intended agents, and avoid indexing logs that may contain secrets, credentials, private prompts, or sensitive reasoning.

Risk: The generated SQLite search.db and WAL files may expose conversation content if left on a shared or weakly protected machine.

Mitigation: Protect the database files with local access controls and delete them when the search index is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larios613-hub/skills/fts5-session-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local SQLite search.db and WAL files when indexing session logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
