## Description: <br>
OpenClaw 数据建表规范与流程指导。当用户需要创建数据仓库表（DDL）时使用，支持 DWS/DWD/DIM/ADS 等层级，引导完成工作空间选择、表命名、字段定义、分区策略、生命周期等完整建表流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiangYan0722](https://clawhub.ai/user/JiangYan0722) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers and warehouse developers use this skill to collect table requirements and draft data warehouse DDL following OpenClaw naming, partitioning, storage, and lifecycle conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDL can reference production workspaces or define incorrect table names, fields, partitions, lifecycle settings, or storage choices. <br>
Mitigation: Review workspace, table name, partitioning, lifecycle, field definitions, and comments before running DDL in any real database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JiangYan0722/ddlsop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with SQL DDL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before use in any database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
