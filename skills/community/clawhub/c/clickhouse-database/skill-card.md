## Description: <br>
Provides guidance for using clickhouse-client to connect to ClickHouse databases, run queries and data changes, inspect schemas, execute SQL files, and format results as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[429668385](https://clawhub.ai/user/429668385) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to operate ClickHouse through CLI commands for analytics queries, schema inspection, import and export tasks, and controlled database maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose SQL commands that modify or delete database data. <br>
Mitigation: Use read-only or least-privilege database roles by default and manually approve INSERT, ALTER UPDATE, ALTER DELETE, and multiquery or script execution. <br>
Risk: Database commands can target the wrong host, database, or output path. <br>
Mitigation: Verify the host, database, and connection settings before execution, and avoid exporting sensitive query results to shared temporary paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/429668385/clickhouse-database) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, SQL, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are command proposals and operational guidance; database results depend on the user's ClickHouse environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
