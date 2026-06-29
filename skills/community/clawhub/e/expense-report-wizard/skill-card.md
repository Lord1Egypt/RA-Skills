## Description: <br>
Expense Report Wizard helps agents organize business travel reimbursement materials by extracting invoice data, grouping expenses, reconstructing itineraries, generating reimbursement reports, and checking policy-based compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and finance operations teams use this skill to prepare business travel reimbursement packages from invoice photos, local folders, or text descriptions. It is intended to produce organized expense records, itinerary logs, reimbursement forms, and compliance review notes for human review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive reimbursement data, including invoices, company names, local invoice folders, and finance policy text. <br>
Mitigation: Use it only with reimbursement materials the user is comfortable sharing with the assistant, and review generated reports before finance submission. <br>
Risk: Connected OCR, online document, calendar, or enterprise messaging integrations may process business expense data outside the chat environment. <br>
Mitigation: Review and authorize each connected integration before enabling enhanced OCR, document export, schedule lookup, or notification workflows. <br>
Risk: OCR extraction, compliance checks, and tax-related summaries can be incomplete or incorrect, especially when company policy or invoice details are missing. <br>
Mitigation: Require human review, ask users to provide finance policy for threshold checks, and avoid treating the skill as final approval, invoice authenticity verification, or tax advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/expense-report-wizard) <br>
- [Source repository from server-resolved provenance](https://github.com/Sheyuy/expense-report-wizard) <br>
- [Publisher profile](https://clawhub.ai/user/sheyuy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, tables, structured text, CSV-style exports, shell command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include reimbursement reports, itinerary logs, compliance summaries, file-renaming previews, and optional export instructions; financial thresholds depend on user-provided policy.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
