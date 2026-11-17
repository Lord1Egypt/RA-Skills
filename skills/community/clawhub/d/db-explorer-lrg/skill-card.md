## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect database schemas, run bounded queries, diagnose database health, and export or migrate data across PostgreSQL, MySQL, SQLite, MongoDB, and Redis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database export, restore, import, and migration commands can expose or alter data if copied directly.

Mitigation: Use least-privileged, non-production credentials where possible, confirm the exact target database before running data-changing commands, and review generated commands before execution.

Risk: Credentials may be exposed when passwords are pasted into command lines or shared output locations.

Mitigation: Prefer environment variables or private secret handling for credentials, avoid echoing real passwords, and write exports to private, access-controlled locations instead of shared temporary paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-lrg)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lrg913427-dot)
- [MongoDB Shell Documentation](https://www.mongodb.com/docs/shell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and query snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database CLI commands, SQL or shell snippets, schema summaries, export guidance, and safety checks.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
