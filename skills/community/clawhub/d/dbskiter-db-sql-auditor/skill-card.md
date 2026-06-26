## Description: <br>
Audits SQL across its lifecycle, including standards checks, performance assessment, and DDL impact analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to run dbskiter audits for SQL statements, SQL files, DDL changes, optimization, index recommendations, execution-plan analysis, cost estimation, and SQL rewrite guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audits may be run against the wrong database or environment. <br>
Mitigation: Confirm the intended database and environment before executing dbskiter commands. <br>
Risk: SQL, DDL, or SQL files may contain production-sensitive information. <br>
Mitigation: Review inputs first and use only authorized files and database contexts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/magicczc/dbskiter-db-sql-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/magicczc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SQL or DDL review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on a local dbskiter installation and the selected database name.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
