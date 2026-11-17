## Description:

Imports OpenClaw session JSONL conversation history into a local SQLite database and lets an agent help users search those archived conversations with SQLite FTS5 or LIKE fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shu0yu](https://clawhub.ai/user/shu0yu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to import local conversation sessions into a searchable SQLite archive, then query prior prompts and assistant replies when reviewing past work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversation history in a plaintext SQLite database that may include sensitive prompts, code, credentials, and assistant replies.

Mitigation: Run it only on a trusted single-user machine, store the database in a private directory, and restrict file permissions on the database file.

Risk: The suggested recurring import can continue archiving future sessions after the initial setup.

Mitigation: Enable scheduled imports only when continuous archiving is intended, review the cron entry periodically, and remove it when the archive is no longer needed.

Risk: Archived conversations remain searchable until the database is deleted or moved.

Mitigation: Delete conversations.db when the archive is no longer needed and avoid placing it in synced or shared folders.

## Reference(s):

- [Database Schema](references/schema.md)
- [ClawHub skill page](https://clawhub.ai/shu0yu/skills/conversations)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration, Text]

**Output Format:** [Markdown with Python command examples and plain text query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads a local SQLite conversation archive; query output is limited by the script's result limit.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
