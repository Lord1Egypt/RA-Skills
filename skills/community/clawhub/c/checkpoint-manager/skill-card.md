## Description:

Checkpoint Manager helps agents persist and recover workflow checkpoint state in PostgreSQL, use SQLite as a disposable local cache, verify consistency, and rebuild cache state after failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations agents use this skill to save, read, list, verify, and rebuild workflow checkpoints across PostgreSQL and SQLite-backed cache paths for crash recovery and workflow state persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint state may be stored in PostgreSQL, local SQLite cache, and generated reports.

Mitigation: Do not store credentials, session tokens, regulated data, or sensitive personal data unless the database, cache, reports, retention, and access controls are approved for that data.

Risk: The SQLite cache is intentionally lossy and can be stale, damaged, or missing.

Mitigation: Use PostgreSQL reads for authoritative recovery or final confirmation, and run the rebuild and integrity verification flows when cache consistency matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/checkpoint-manager)
- [Business Rules](references/business_rules.md)
- [Error Codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with command examples and JSON request/response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PostgreSQL as the authoritative checkpoint source and SQLite as a lossy local cache.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
