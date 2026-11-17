## Description:

Memory Graph helps agents maintain a local, file-based personal knowledge graph using markdown nodes, YAML frontmatter, derived SQLite indexes, and supporting maintenance scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afgonullu](https://clawhub.ai/user/afgonullu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and agents use this skill to preserve context about people, projects, tools, concepts, places, and decisions across agent sessions. It supports querying, briefing generation, graph validation, index rebuilding, backfill suggestions, visualization, and optional git-backed change history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a persistent local memory store that may contain sensitive personal or project information.

Mitigation: Keep the memory directory private, do not store secrets or sensitive personal details, and review files before committing or sharing the repository.

Risk: Optional semantic backfill can invoke QMD shell commands.

Mitigation: Use the documented --no-qmd option until the shell invocation concern identified by the security guidance is resolved.

Risk: Generated graph HTML may expose unsafe behavior when opened with untrusted graph content.

Mitigation: Open generated graph HTML only for trusted local graph content until the HTML injection and CDN concerns in the security guidance are addressed.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Demo Graph HTML](docs/demo-graph.html)
- [QMD semantic search](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file paths, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+ for built-in node:sqlite; QMD semantic search is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
