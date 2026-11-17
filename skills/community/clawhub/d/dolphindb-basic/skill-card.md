## Description:

Guides agents through DolphinDB CRUD workflows, including database and table creation, data insertion, querying, updates, deletion, and distributed or in-memory table management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to have an agent draft DolphinDB setup checks, Python SDK calls, and CRUD examples for distributed and in-memory database tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sourcing setup scripts from a separate dolphindb-skills package.

Mitigation: Review and trust the separate setup scripts before installing or using this skill.

Risk: Examples include default DolphinDB administrator credentials.

Mitigation: Change any default admin password and use least-privileged database accounts.

Risk: Examples include destructive DELETE, DROP, and partition-removal operations.

Mitigation: Require explicit backups, target checks, and operator confirmation before running destructive examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ugpoor/skills/dolphindb-basic)
- [DolphinDB Official Site](https://www.dolphindb.cn/)
- [DolphinDB Documentation Center](https://docs.dolphindb.cn/zh/)
- [DolphinDB Create Database and Table](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html)
- [DolphinDB Insert Data](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/insert_data.html)
- [DolphinDB Queries](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/queries.html)
- [DolphinDB Modify Data](https://docs.dolphindb.cn/zh/db_distr_comp/mod_data.html)
- [DolphinDB Drop Database and Table](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/drop_db_tb.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes DolphinDB Python SDK examples and database operation snippets; users should adapt hosts, credentials, and target databases.]

## Skill Version(s):

1.4.0 (source: server release metadata; changelog: v1.4.0 添加强制环境检测流程，支持全局包装器调用)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
