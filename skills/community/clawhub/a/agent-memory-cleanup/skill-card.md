## Description:

Agent Memory Cleanup audits and cleans long-term agent memory files by removing or flagging stale task notes, duplicate or conflicting preferences, and suspected secrets while requiring approval before writes and creating recoverable backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep persistent assistant memory focused on stable user preferences and durable context. It helps inspect memory pressure, propose cleanup, redact suspected secrets, preserve backups, and apply approved edits to user-selected memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite persistent memory files.

Mitigation: Require explicit approval before applying edits, review proposed diffs, and keep cleanup scoped to memory files the user names or clearly authorizes.

Risk: Backups may retain secrets removed from the active memory file.

Mitigation: Treat backup files as sensitive, review retention needs after cleanup, and avoid sharing or committing backups.

Risk: Overbroad path discovery could expose unrelated user files.

Mitigation: Limit discovery to user-provided paths, workspace memory files, or configured memory roots, and avoid broad home-directory scans unless explicitly requested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hollis9087/skills/agent-memory-cleanup)
- [Agent Memory Paths](references/agent-paths.md)
- [Classification Rubric](references/classification-rubric.md)
- [Default Rules](references/default-rules.json)
- [MCP Version Guidance](references/mcp-version.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, unified diffs, proposed cleaned memory content, backup paths, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write approved memory edits and proposed cleaned files; apply mode creates timestamped backups before changing a memory file.]

## Skill Version(s):

0.3.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
