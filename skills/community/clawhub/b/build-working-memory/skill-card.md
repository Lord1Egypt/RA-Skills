## Description:

Set up, migrate, or manage a file-based working memory system for an AI agent project, including scaffolding, migration, layered retrieval, structured event indexing, and deterministic temporal support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiyuan](https://clawhub.ai/user/jiyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, file-based working memory to AI agent projects, migrate legacy memory layouts, and retrieve prior session context within token budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist private session data in project memory files.

Mitigation: Keep generated memory files private, avoid committing sensitive memory to shared repositories, and review stored content before sharing a workspace.

Risk: Migration can modify future agent instructions by patching AGENT.md or AGENTS.md.

Mitigation: Run migration with --dry-run first, consider --skip-agent-patch for manual review, and inspect generated backups and patches before use.

Risk: Loaded historical memory can influence current agent behavior even when the stored content is stale or untrusted.

Mitigation: Treat loaded memory as untrusted historical context, add explicit prompt rules for handling it, and fix loader lookups to restrict retrieval to canonical memory/YYYY-MM-DD.md files before hostile or shared use.

## Reference(s):

- [Working Memory Skill on ClawHub](https://clawhub.ai/jiyuan/skills/build-working-memory)
- [Migration Reference](artifact/references/MIGRATION.md)
- [Retrieval Workflow](artifact/references/RETRIEVAL.md)
- [Schema Reference](artifact/references/SCHEMAS.md)
- [Temporal Memory Reference](artifact/references/TEMPORAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, and generated file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-based memory scaffolds, migration steps, retrieval guidance, and configuration instructions for agent projects.]

## Skill Version(s):

1.1.1 (source: server release metadata; target metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
