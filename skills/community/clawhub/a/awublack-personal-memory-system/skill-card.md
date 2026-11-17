## Description:

A local personal memory system that syncs MEMORY.md into a searchable SQLite database and helps an agent answer natural-language questions from stored notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local, queryable personal knowledge base for notes, decisions, and past views. It is intended for OpenClaw-style assistants that can sync Markdown memory entries into SQLite and summarize matching records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent Git sync process may commit private memory notes to durable Git history while the skill also presents itself as local-only.

Mitigation: Inspect the sync script before enabling it, verify the remote repository is yours and private, and confirm you are comfortable with notes being committed.

Risk: Personal memory files can contain secrets or sensitive personal data that are difficult to remove after synchronization.

Mitigation: Avoid storing secrets or highly sensitive data in synchronized notes, and review MEMORY.md, the Obsidian vault, Git history, and sync logs before sharing or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awublack/skills/awublack-personal-memory-system)
- [Publisher profile](https://clawhub.ai/user/awublack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with shell command examples and Python-backed query output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on locally stored MEMORY.md and SQLite records; query results are limited by the bundled retrieval script.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
