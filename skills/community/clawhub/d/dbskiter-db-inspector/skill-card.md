## Description: <br>
数据库实例巡检与报告生成，支持配置检查、性能检查、安全检查、报告生成、智能巡检、异常检测、根因分析、风险预测。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators, SREs, and engineers use this skill to have an agent run dbskiter inspection commands, interpret database health, configuration, performance, storage, security, and capacity findings, and produce reports or follow-up diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run MySQL helper commands that may affect production databases if used without scoping. <br>
Mitigation: Require explicit confirmation of host, database, environment, account, target tables, and whether the requested task is read-only or write-capable before execution. <br>
Risk: Inspection or maintenance workflows may expose broad database access or credentials. <br>
Mitigation: Prefer read-only database users for inspection, use SSL for production connections, and avoid storing broad credentials. <br>
Risk: Database-changing operations such as UPDATE, DELETE, import, export, or schema management can cause data loss or service impact. <br>
Mitigation: Require backups or rollback plans before any write-capable or schema-management command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-db-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to HTML, Markdown, or JSON report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database inspection, report generation, anomaly detection, root-cause analysis, and risk prediction commands for dbskiter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
