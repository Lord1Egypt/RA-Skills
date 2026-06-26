## Description: <br>
智能财务报销助手帮助用户接收、解析、归档和跟踪多公司发票、无发票费用与重要财务事项，并生成待报销和待处理提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who manage finance work across multiple companies use this skill to track invoice-backed reimbursements, expenses without invoices, and important tax or accounting tasks. It helps an agent parse invoice files, maintain local Markdown ledgers, classify invoice headers, and prepare recurring reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store invoice files, tax identifiers, company mappings, reimbursement ledgers, and reminder records in a local finance workspace. <br>
Mitigation: Use a private directory with appropriate filesystem permissions and review parsed invoice fields before sharing or syncing records. <br>
Risk: Recurring cron templates can repeatedly read and update finance records. <br>
Mitigation: Enable scheduled jobs only when recurring reminders are intended, and periodically review the target files and delivery settings. <br>
Risk: Generated reimbursement workflows may involve sharing finance details through Feishu or related tools. <br>
Mitigation: Verify recipients, document permissions, and packaged files before sending reimbursement materials. <br>


## Reference(s): <br>
- [Finance Assistant ClawHub Listing](https://clawhub.ai/afeicn/finance-assistant) <br>
- [Invoice Header Mapping Reference](references/headers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, Markdown table records, and YAML cron templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local finance workspace files and invoice originals under ~/finance or a user-selected finance directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
