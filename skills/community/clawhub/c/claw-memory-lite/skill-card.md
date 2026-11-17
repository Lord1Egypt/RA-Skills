## Description:

Manage and query an agent's distilled long-term memory with lightweight SQLite-backed tools and automated daily extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timothysong0w0](https://clawhub.ai/user/timothysong0w0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to extract daily memory notes into a local SQLite database, query stored memory by keyword or category, and schedule recurring memory maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can perform daily local writes to MEMORY.md and the SQLite database.

Mitigation: Do not enable heartbeat or cron automation until the release is reviewed, and back up MEMORY.md before first use.

Risk: The local insight.db database may contain copied memory records, configuration details, and credential-related notes in plaintext.

Mitigation: Restrict database file permissions and avoid storing secrets in memory files.

Risk: Mutable install paths can change what code is installed later.

Mitigation: Install from a pinned release or commit and avoid the mutable curl install path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timothysong0w0/skills/claw-memory-lite)
- [Artifact README](artifact/README.md)
- [Installation Guide](artifact/docs/installation.md)
- [Integration Guide](artifact/docs/integration.md)
- [API Reference](artifact/docs/api.md)
- [Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python/SQLite examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory query results, extraction summaries, database setup guidance, heartbeat or cron configuration, and maintenance reports.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
