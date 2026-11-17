## Description:

Generate, manage, and track professional invoices with payment terms, recurring billing, overdue automation, and financial reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

External users, operators, and business teams use this skill to create invoices, manage clients, track payments, generate reminders, and review revenue status from structured invoice and client records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive client, tax, invoice, and payment reference data may be stored by the agent.

Mitigation: Keep records in a protected datastore or locked-down files, and avoid storing tax IDs or payment references unless necessary.

Risk: Automatic invoice creation, reminders, recurring billing, or payment recording could create incorrect billing actions.

Mitigation: Require explicit confirmation before creating invoices, sending reminders, enabling recurring billing, or recording payments.

Risk: Scheduled or auto-send behavior can contact recipients without enough controls.

Mitigation: Do not enable cron, heartbeat, daily memory logging, or auto-send behavior until recipients and review steps are clearly controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-invoice-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown, structured text, and YAML/CSV/JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces invoice templates, client and invoice ledger structures, reminder messages, recurring billing routines, and financial report summaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
