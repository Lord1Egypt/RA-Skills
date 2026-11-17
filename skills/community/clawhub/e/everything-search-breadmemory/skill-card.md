## Description:

Provides a local Everything/es.exe file-search workflow with breadcrumb knowledge storage, Ebbinghaus review scheduling, and topology-based knowledge association.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search local Windows files, summarize selected findings into persistent breadcrumb notes, review those notes on an Ebbinghaus schedule, and explore related notes through a generated knowledge graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local search workflows may lead to matched file contents being read and summarized.

Mitigation: Show search results first and require user confirmation before ingesting or summarizing file contents.

Risk: Breadcrumb notes, source paths, review logs, topology data, and recovery backups are stored persistently.

Mitigation: Review and restrict the data directory and backup files when stored knowledge or source paths may be sensitive.

Risk: The skill can download an Everything CLI executable when es.exe is unavailable.

Mitigation: Prefer a manually installed and verified es.exe, or require explicit approval before any download.

Risk: The workflow describes scheduled task setup for recurring search, review, or graph updates.

Mitigation: Require explicit user approval before creating or modifying scheduled tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/everything-search-breadmemory)
- [Everything documentation](https://www.voidtools.com)
- [Workflow](references/workflow.md)
- [Script reference](references/script-reference.md)
- [Agent behavior](references/agent-behavior.md)
- [Permissions](references/permissions.md)
- [Data storage](references/data-storage.md)
- [FAQ](references/faq.md)
- [Antipatterns](references/antipatterns.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and knowledge-management commands may create local JSON data, review logs, topology files, and recovery backups.]

## Skill Version(s):

1.5.1 (source: server release metadata, skill frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
