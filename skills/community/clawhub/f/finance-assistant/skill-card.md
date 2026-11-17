## Description:

智能财务事项与报销跟踪系统。它能够对多公司、多发票抬头进行智能化管理，从发票文件的接收、解析、分类存储到最终报销，提供一站式全生命周期的跟踪与提醒服务。支持PyMuPDF智能发票解析归档、发票缺漏智能补录及重要财务日程提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and assistants managing business expenses use this skill to track invoice files, reimbursement status, no-invoice expenses, and important finance deadlines across multiple companies and invoice headers. It also guides weekly reminders and invoice parsing checks so unresolved items can be followed up consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains sensitive invoice, reimbursement, and finance deadline records in local files.

Mitigation: Use a dedicated finance directory, review file permissions, and avoid exposing the directory through shared sync or chat channels unless approved.

Risk: Weekly reminder automation may read finance records, send summaries, and update reminder counts.

Mitigation: Confirm the reminder schedule, delivery destination, read scope, and any write behavior before enabling automation.

Risk: Invoice parsing can confuse buyer and seller fields in Chinese electronic invoices because text extraction may not preserve the visual column layout.

Mitigation: Verify company names and tax IDs against references/headers.md and ask the user to confirm when extracted invoice details conflict.

Risk: Invoice retention choices can affect records that may be needed later.

Mitigation: Agree on deletion and retention rules before removing old invoice files.

## Reference(s):

- [发票抬头 → 公司映射表](references/headers.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown records, concise summaries, invoice file links, and optional YAML cron templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local finance records under ~/finance/ or a user-selected finance directory.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
