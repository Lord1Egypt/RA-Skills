## Description: <br>
Design partition schemes, select partition keys, create GSI and CCI indexes, and write or adapt SQL for PolarDB-X 2.0 Enterprise Edition AUTO mode databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to design PolarDB-X table partitioning, indexes, migrations, compatibility rewrites, and query diagnostics for Enterprise Edition AUTO mode workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes Alibaba Cloud CLI credential and account-administration guidance beyond the stated SQL design purpose. <br>
Mitigation: Do not provide cloud account keys or run Aliyun CLI setup from this skill unless that capability is intentionally required; use least-privilege credentials and explicit user confirmation. <br>
Risk: DDL, partition changes, TTL cleanup, and EXPLAIN ANALYZE commands can affect production data or workload behavior. <br>
Mitigation: Require backups, staging validation, and explicit confirmation before applying generated SQL or diagnostic commands to a live PolarDB-X environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-polardbx-sql) <br>
- [PolarDB-X SQL skill instructions](artifact/SKILL.md) <br>
- [Acceptance criteria](artifact/references/acceptance-criteria.md) <br>
- [PolarDB-X CREATE TABLE](artifact/references/create-table.md) <br>
- [PolarDB-X partition design best practices](artifact/references/partition-design-best-practice.md) <br>
- [Primary keys and unique keys](artifact/references/primary-key-unique-key.md) <br>
- [PolarDB-X Global Secondary Index](artifact/references/gsi.md) <br>
- [PolarDB-X Clustered Columnar Index](artifact/references/cci.md) <br>
- [PolarDB-X sequence](artifact/references/sequence.md) <br>
- [PolarDB-X distributed transactions](artifact/references/transactions.md) <br>
- [PolarDB-X and MySQL compatibility notes](artifact/references/mysql-compatibility-notes.md) <br>
- [PolarDB-X EXPLAIN diagnostics](artifact/references/explain.md) <br>
- [PolarDB-X TTL tables and cold data archiving](artifact/references/ttl-table.md) <br>
- [PolarDB-X online DDL and lock-free DDL operations](artifact/references/online-ddl.md) <br>
- [PolarDB-X efficient pagination best practices](artifact/references/pagination-best-practice.md) <br>
- [PolarDB-X range partition auto-add partitions](artifact/references/auto-add-range-parts.md) <br>
- [Aliyun CLI installation and configuration guide](artifact/references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PolarDB-X SQL proposals, compatibility notes, diagnostic commands, and configuration guidance requiring user confirmation before execution.] <br>

## Skill Version(s): <br>
0.0.2 (source: server-resolved release metadata; artifact frontmatter metadata.version is 0.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
