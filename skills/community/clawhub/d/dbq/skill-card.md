## Description: <br>
DBQ helps agents run configured SQL queries and controlled database writes across dev, test, and prod aliases for SQLite, MySQL, MariaDB, and PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinpengfei](https://clawhub.ai/user/yinpengfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use DBQ to let coding agents inspect schemas, run read queries, and perform permission-gated database writes through predefined aliases without sharing raw connection details in prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact database writes or schema changes when configured with write or DDL permissions. <br>
Mitigation: Use read-only database accounts by default, keep production connections read-only unless explicitly needed, and require dry-run review before writes. <br>
Risk: Credentials and raw SQL can be exposed through local environment files, terminal output, or query logs. <br>
Mitigation: Prefer Keychain or managed secrets over .env files, avoid printing secrets in logged terminals, and treat the logs directory as sensitive. <br>
Risk: Setting DB_QUERY_ASSUME_YES=1 can bypass production write confirmations in automated agent runs. <br>
Mitigation: Do not set DB_QUERY_ASSUME_YES=1 for production unless the automation path is tightly controlled and independently reviewed. <br>


## Reference(s): <br>
- [DBQ ClawHub Skill Page](https://clawhub.ai/yinpengfei/skills/dbq) <br>
- [README_EN.md](README_EN.md) <br>
- [Driver Dependencies](references/drivers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output may be table, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Database access depends on user-provided aliases and credentials; queries are logged locally by the tool.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
