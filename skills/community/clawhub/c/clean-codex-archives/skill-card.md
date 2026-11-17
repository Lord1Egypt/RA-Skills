## Description:

Safely inspects and removes locally archived Codex conversation data across Windows, macOS, and Linux, including archived JSONL files, archived SQLite thread records, related logs, and stale session index entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunarcache](https://clawhub.ai/user/lunarcache)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to inventory and, after explicit authorization, delete archived local Codex history while preserving active sessions and checking database and session-index consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archived local Codex history can be permanently removed when cleanup is applied.

Mitigation: Run the dry run first, review the reported counts, and use --apply only after explicit authorization.

Risk: Cleanup touches local SQLite databases and session index files.

Mitigation: Preserve active sessions, reject malformed session-index data, retry only after closing processes that lock the databases, and verify SQLite quick_check after changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry run by default; destructive cleanup requires --apply; optional --vacuum compacts SQLite databases.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
