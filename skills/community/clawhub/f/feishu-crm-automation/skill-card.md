## Description: <br>
飞书CRM自动化技能。当用户提到客户管理、销售跟进、CRM录入、飞书表格自动填充、跟进提醒、生成本周客户报告时使用。功能：客户信息录入多维表格、超期未跟进自动提醒、客户周报生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanderen](https://clawhub.ai/user/wanderen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and CRM users use this skill to enter customer information into Feishu Bitable, find customers overdue for follow-up, and generate weekly customer summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a hard-coded Feishu Bitable app_token and table_id that could receive customer data. <br>
Mitigation: Replace the default Bitable target with an authorized workspace table before use, and verify table ownership and permissions. <br>
Risk: Customer names, contact details, and requirements may be written to Feishu during create or update actions. <br>
Mitigation: Require user confirmation before writes and avoid sending real customer data unless the Feishu app and table are approved for that data. <br>


## Reference(s): <br>
- [跟进提醒逻辑](references/跟进提醒逻辑.md) <br>
- [周报生成逻辑](references/周报生成逻辑.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown summaries with Feishu Bitable tool calls and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu Bitable app_token, table_id, field mappings, millisecond timestamps, and Asia/Shanghai time.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
