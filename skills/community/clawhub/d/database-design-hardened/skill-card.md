## Description:

Database design helper for table design, normalization, indexing strategy, migration scripts, test data, and ER diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft database schemas, indexes, migrations, seed data, and ER diagram descriptions for review before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or migration guidance may be unsafe if applied directly to a live database.

Mitigation: Review all generated SQL manually, test in a non-production environment, and do not pipe output directly into a database or migration pipeline.

Risk: The generic script can log command arguments locally, which may expose secrets, connection strings, or sensitive query text.

Mitigation: Avoid passing secrets, connection strings, or sensitive query text as script arguments.

Risk: Generated SQL may include unsafe dynamic identifiers or draft statements that need database-specific validation.

Mitigation: Use parameterized queries for values, allowlist dynamic identifiers, and validate generated SQL against the target database engine before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/database-design-hardened)
- [BytesAgain homepage](https://bytesagain.com)
- [Faberlens database-design safety report](https://faberlens.ai/explore/database-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft database design guidance and SQL artifacts for manual review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
