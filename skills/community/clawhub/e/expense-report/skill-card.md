## Description: <br>
Generates structured expense reports from receipt, invoice, and everyday spending descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Independent professionals, freelancers, contractors, interns, and external sales workers use this skill to turn expense lists or receipt text into categorized reimbursement reports. It totals spending by category, separates reimbursable and personal expenses, and can produce simplified or formal report text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense descriptions and receipts may contain sensitive personal, financial, or business information. <br>
Mitigation: Provide only the receipt details needed for the report and avoid unnecessary sensitive information. <br>
Risk: The skill can write files when the agent supports file-writing tools. <br>
Mitigation: Ask the agent to return the report inline unless a file output is explicitly needed. <br>
Risk: Automatically inferred categories, dates, currencies, or reimbursement status may be wrong when input details are incomplete. <br>
Mitigation: Review totals, categories, dates, and reimbursable flags before submitting the report for reimbursement or accounting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreataide86/expense-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown or plain text expense reports with totals, categories, reimbursement status, and optional email-ready wording] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports simplified and complete report styles, BRL and USD amounts, category summaries, and reimbursable versus personal expense separation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
