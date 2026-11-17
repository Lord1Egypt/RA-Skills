## Description:

Intelligent database import from .csv and .sql dumps into MySQL, MariaDB, and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarbcs1-prog](https://clawhub.ai/user/jarbcs1-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to analyze source and destination schemas, suggest column mappings, and import CSV or SQL dump data into MySQL, MariaDB, or SQLite. It is intended for data migration and ingestion workflows where mappings and database changes are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run high-impact database changes and execute SQL dumps that may alter or destroy data.

Mitigation: Use only trusted CSV and SQL files, prefer a staging database, and take verified backups before running imports or SQL dumps.

Risk: Credential examples use command-line passwords and root-like accounts, which can expose secrets or over-privilege import operations.

Mitigation: Avoid putting database passwords directly in command lines and use least-privilege database accounts.

Risk: Automated column mapping suggestions may be incorrect.

Mitigation: Review suggested mappings and verify column types before executing imports.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON mapping examples, and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces schema analysis, column mapping suggestions, and import commands for local database workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
