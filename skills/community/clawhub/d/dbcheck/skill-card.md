## Description: <br>
DBCheck runs health inspections for MySQL, PostgreSQL, Oracle, SQL Server, DM8, TiDB, IvorySQL, GBase 8s, YashanDB, and KingbaseES databases, applies 130+ risk rules, and generates professional inspection reports for DBAs and operations teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fiyo](https://clawhub.ai/user/fiyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DBAs, operations engineers, and authorized database administrators use this skill to collect database and optional host health metrics, identify operational risks, and generate local inspection reports with suggested remediation steps. It is intended for authorized database environments only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles database credentials and may handle SSH credentials for optional host metric collection. <br>
Mitigation: Use dedicated read-only database accounts where possible, avoid command-line password flags, and provide SSH access only for authorized target hosts. <br>
Risk: Generated remediation SQL and optimization guidance may be inappropriate for a production workload if applied without review. <br>
Mitigation: Review all generated repair SQL and recommendations with the responsible DBA or operations owner before executing them in production. <br>
Risk: AI analysis can expose database inspection data if routed to an online or OpenAI-compatible endpoint. <br>
Mitigation: Keep AI analysis disabled or local-only unless the inspection data is approved to leave the environment. <br>
Risk: A Web UI exposed beyond localhost could broaden access to database inspection workflows and collected results. <br>
Mitigation: Bind any Web UI to localhost unless a reviewed deployment plan adds authentication, network controls, and operational monitoring. <br>


## Reference(s): <br>
- [DBCheck ClawHub release](https://clawhub.ai/fiyo/skills/dbcheck) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact security notes](artifact/security.md) <br>
- [Oracle Instant Client documentation](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html) <br>
- [Microsoft ODBC Driver for SQL Server documentation](https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated inspection reports are DOCX or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written locally under the skill scripts reports directory; history and logs may also be written locally.] <br>

## Skill Version(s): <br>
2.6.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
