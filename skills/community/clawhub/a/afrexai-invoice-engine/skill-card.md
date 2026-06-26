## Description: <br>
Generate, manage, and track professional invoices with payment terms, recurring billing, overdue automation, and financial reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, business operators, and agents use this skill to create invoices, manage client billing records, track payments, handle recurring billing, generate overdue reminders, and review revenue reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic billing, overdue reminders, cron jobs, or client-facing invoice communication could affect customers or business records without strong approval controls. <br>
Mitigation: Require manual review and explicit approval before enabling auto-send, overdue reminders, scheduled jobs, or any client-facing invoice communication. <br>
Risk: Client and invoice YAML files may contain sensitive business, tax, payment, or contact details. <br>
Mitigation: Keep these files in a private workspace and avoid storing unnecessary tax or payment details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-invoice-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown, YAML examples, invoice text templates, reminder email drafts, CSV/JSON export guidance, and reporting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce client and invoice records, recurring billing schedules, payment reminders, aging reports, and financial summaries for manual review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
