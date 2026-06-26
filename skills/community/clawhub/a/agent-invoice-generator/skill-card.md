## Description: <br>
Generates professional invoices from natural language or structured invoice data, including line items, tax, discounts, currencies, recurring invoice setup, payment tracking, and PDF or HTML output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and business operators use this skill to create invoices, record payment status, and manage local invoice data through an agent-driven command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores business contact details, client names, invoice notes, amounts, and payment status in local files under the user's home directory. <br>
Mitigation: Use it only on trusted machines, protect the home directory, and avoid entering sensitive client information unless local storage is acceptable. <br>
Risk: Invoice amounts, taxes, discounts, due dates, and payment status may be incorrect if natural-language input is parsed incorrectly or source data is incomplete. <br>
Mitigation: Review generated invoice records and files before sending them to clients or recording payment status. <br>
Risk: Recurring invoices or email delivery can automate business actions beyond simple local file generation. <br>
Mitigation: Require explicit user confirmation before configuring cron-based recurring invoices or using any separate email skill to send invoices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/agent-invoice-generator) <br>
- [Publisher profile](https://clawhub.ai/user/Johnnywang2001) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summary with shell commands; generated invoice records as JSON and invoices as PDF or HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores configuration under ~/.openclaw and invoice outputs under ~/Documents/Invoices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
