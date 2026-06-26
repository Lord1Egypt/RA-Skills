## Description: <br>
智能收支手帐。记录个人和家庭日常收支、管理固定支出、生成月度汇总报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiss1952](https://clawhub.ai/user/kiss1952) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and families use this skill to record income and expenses in natural language, manage recurring costs, query spending, and generate monthly finance summaries in local workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and modifies sensitive financial records in the workspace. <br>
Mitigation: Confirm the storage location before use, avoid account numbers or other unnecessary identifiers, and review generated records before relying on them. <br>
Risk: Broad natural-language triggers could record or modify finance data without enough upfront consent. <br>
Mitigation: Use explicit commands for recording, correction, deletion, and reporting, and confirm ambiguous transactions before writing files. <br>
Risk: Retention and cleanup expectations are not fully defined in the artifact. <br>
Mitigation: Confirm how to delete or correct entries before entering sensitive personal or family finance details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kiss1952/buddy-bills) <br>
- [支出分类体系](references/categories.md) <br>
- [数据目录结构与文件格式规范](references/data-schema.md) <br>
- [固定支出配置规则](references/fixed-costs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance and structured YAML finance records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and updates local finance records under finance-records/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
