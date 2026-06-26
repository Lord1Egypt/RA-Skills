## Description: <br>
报销助手 helps users organize business entertainment and travel reimbursement materials by recognizing invoices and vouchers, classifying expenses, generating reimbursement summaries, and renaming receipt files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esther-muye](https://clawhub.ai/user/esther-muye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and reimbursement preparers use this skill to manage business entertainment and travel reimbursement workflows, including invoice extraction, voucher classification, reimbursement summary generation, and receipt file organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt files may be renamed in place and copied into a reimbursement directory. <br>
Mitigation: Test the workflow on sample files first, keep backups of important receipts, and check for filename conflicts before processing a large folder. <br>
Risk: Invoice, voucher, or image extraction may produce incorrect dates, amounts, vendors, or expense categories. <br>
Mitigation: Review extracted fields and generated reimbursement summaries before submitting materials to an expense system. <br>
Risk: Transportation subsidy rules and reimbursement periods may differ from a user's company policy. <br>
Mitigation: Confirm subsidy amounts, reimbursement windows, and category rules against the applicable company policy before use. <br>


## Reference(s): <br>
- [报销助手 reference document](references/数据结构.md) <br>
- [ClawHub skill page](https://clawhub.ai/esther-muye/expense-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, generated reimbursement summaries, structured records, and local file operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rename original receipt files and copy them into a local reimbursement directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
