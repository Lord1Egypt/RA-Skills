## Description: <br>
Inspects Hive Metastore metadata through DB or Thrift connections, producing full or incremental reports with table metadata, storage sizes, DDL, and change records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data platform engineers use this skill to inventory Hive tables and identify metadata, schema, data, or partition changes before planning lakehouse migration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is mostly for inspection but includes migration-script and overwrite-SQL generators that can go beyond read-only metadata review. <br>
Mitigation: Install only when that broader behavior is intended, use read-only Metastore credentials for inspection, and review generated rclone scripts and Paimon SQL before execution. <br>
Risk: Configuration profiles or generated scripts may contain credentials or storage access details. <br>
Mitigation: Prefer environment variables for secrets, avoid saving plaintext credentials, and inspect generated files before sharing or running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-lhm-inspect-hive-metastore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, CSV reports, SQL DDL, generated rclone shell scripts, and Paimon SQL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full exploration produces summary_report.csv and per-table DDL files; incremental exploration produces metastore_delta.csv.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
