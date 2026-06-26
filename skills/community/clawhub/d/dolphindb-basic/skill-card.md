## Description: <br>
Provides guidance and examples for basic DolphinDB CRUD operations, including creating databases and tables, inserting data, querying, updating, and deleting records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to draft and adapt DolphinDB scripts for common database setup, table management, CRUD operations, and partitioned data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples normalize default administrator credentials for DolphinDB access. <br>
Mitigation: Replace default credentials with a rotated, least-privilege account before use. <br>
Risk: The skill includes DELETE, DROP, bulk UPDATE, and partition deletion examples that can irreversibly modify data. <br>
Mitigation: Require explicit human confirmation, verified backups, and a controlled environment before running destructive examples. <br>
Risk: The skill references shared helper scripts for DolphinDB environment setup. <br>
Mitigation: Review the helper scripts in the local DolphinDB skill suite before sourcing or executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/dolphindb-basic) <br>
- [DolphinDB website](https://www.dolphindb.cn/) <br>
- [DolphinDB documentation center](https://docs.dolphindb.cn/zh/) <br>
- [Create databases and tables](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/create_db_tb.html) <br>
- [Insert data](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/insert_data.html) <br>
- [Queries](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/queries.html) <br>
- [Update data](https://docs.dolphindb.cn/zh/db_distr_comp/mod_data.html) <br>
- [Drop databases and tables](https://docs.dolphindb.cn/zh/db_distr_comp/db_oper/drop_db_tb.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, DolphinDB, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may include database-mutating commands that require human review before execution.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
