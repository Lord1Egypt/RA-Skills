## Description:

数据库安全审计，支持 SQL 注入检测、敏感数据扫描、权限审计、登录安全监控、审计日志分析、密码策略检查和配置安全审计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and security engineers use this skill to run dbskiter database security checks and interpret structured findings for remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect sensitive database contents, users, permissions, logs, login IPs, and weak-password indicators.

Mitigation: Use it only against databases the operator administers, confirm the database name and scope before execution, prefer table-scoped scans, and treat all findings as confidential.

Risk: Broad database security scans can expose more data than needed for the user's immediate question.

Mitigation: Limit scans with available table, user, and time-window parameters when a narrower audit is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-security)
- [Publisher profile](https://clawhub.ai/user/magicczc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured result interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference database names, table scopes, time windows, users, SQL statements, and dbskiter security subcommands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
