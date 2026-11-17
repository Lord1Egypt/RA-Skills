## Description:

OpenClaw 数据建表规范与流程指导。当用户需要创建数据仓库表（DDL）时使用，支持 DWS/DWD/DIM/ADS 等层级，引导完成工作空间选择、表命名、字段定义、分区策略、生命周期等完整建表流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyan0722](https://clawhub.ai/user/jiangyan0722)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to guide OpenClaw-style data warehouse DDL creation, including workspace selection, table naming, field definitions, partitioning, storage format, and lifecycle settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DDL may contain incorrect workspace, table naming, partitioning, storage format, or lifecycle settings.

Mitigation: Review generated DDL before running it in a database, especially workspace, table name, partitioning, storage format, and lifecycle settings.

Risk: Users who cannot read Chinese may misapply the skill's DDL guidance.

Mitigation: Install and use the skill only when the user or reviewer is comfortable with Chinese-language data warehouse guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language DDL guidance; generated DDL should be reviewed before database execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
