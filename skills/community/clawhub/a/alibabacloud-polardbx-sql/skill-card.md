## Description:

Design partition schemes, select partition keys, create GSI, and write SQL for PolarDB-X 2.0 Enterprise Edition AUTO mode databases, handling PolarDB-X vs MySQL differences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to design and review PolarDB-X 2.0 Enterprise Edition AUTO mode schemas, indexes, migrations, SQL compatibility changes, and slow-query diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Aliyun CLI guide expands the skill beyond SQL guidance into credential setup and machine-wide binary installation.

Mitigation: Review CLI instructions before use; avoid unverified latest binary downloads, avoid sudo or system-wide installation unless necessary, and prefer least-privilege short-lived credentials.

Risk: Generated SQL examples can include production-impacting operations such as partition drops, TTL cleanup, DDL changes, and execution-based EXPLAIN modes.

Mitigation: Require explicit confirmation, backups, and review before running destructive or runtime-executing SQL in production environments.

Risk: Cloud secrets may be exposed if users place credentials directly on command lines or in shared configuration.

Mitigation: Use secure credential storage, avoid command-line secrets, rotate access keys, and scope permissions to the minimum required.

## Reference(s):

- [CREATE TABLE syntax and table types](references/create-table.md)
- [Partition design best practices](references/partition-design-best-practice.md)
- [Primary key and unique key rules](references/primary-key-unique-key.md)
- [Global Secondary Index guidance](references/gsi.md)
- [Clustered Columnar Index guidance](references/cci.md)
- [Sequence guidance](references/sequence.md)
- [Distributed transactions](references/transactions.md)
- [MySQL compatibility notes](references/mysql-compatibility-notes.md)
- [EXPLAIN diagnostics](references/explain.md)
- [TTL tables and cold data archiving](references/ttl-table.md)
- [Online DDL and lock-free operations](references/online-ddl.md)
- [Efficient pagination best practices](references/pagination-best-practice.md)
- [Range partition auto-add partitions](references/auto-add-range-parts.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Aliyun CLI installation and configuration guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compatibility notes, version and mode checks, risk warnings, and stepwise database migration guidance.]

## Skill Version(s):

0.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
