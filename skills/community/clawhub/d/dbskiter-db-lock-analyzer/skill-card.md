## Description:

Analyzes database locks, detects deadlocks, traces lock wait chains, and guides dbskiter lock commands for MySQL, PostgreSQL, and Oracle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect active locks, identify deadlocks, trace blocking chains, and prepare lock reports while working with dbskiter-supported databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction termination is a privileged database operation and an incorrect kill recommendation could disrupt production work.

Mitigation: Require human confirmation before running lock kill commands, verify the database name and transaction ID, and use production procedures for incident response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-lock-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database lock statistics, deadlock details, wait-chain analysis, and transaction termination recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
