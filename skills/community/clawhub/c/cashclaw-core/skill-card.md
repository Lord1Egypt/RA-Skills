## Description: <br>
The business brain of CashClaw. Orchestrates mission lifecycle, client communication, revenue tracking, and delegates work to specialized skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate paid CashClaw missions from client intake through quoting, execution, delivery, invoicing, follow-up, and revenue logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores client mission records, business records, and client-facing messages as part of its stated purpose. <br>
Mitigation: Review client data before it is saved and periodically delete old ~/.cashclaw records that are no longer needed. <br>
Risk: Invoices, payment links, deliverables, and follow-up messages may be sent to clients. <br>
Mitigation: Confirm recipients, pricing, invoice details, deliverables, and message content before sending anything externally. <br>
Risk: Delegated CashClaw skills may fail or produce incomplete work during mission execution. <br>
Mitigation: Log failures, retry once, escalate blocked missions to an operator, and do not charge for undelivered work. <br>


## Reference(s): <br>
- [Cashclaw Core on ClawHub](https://clawhub.ai/andreataide86/cashclaw-core) <br>
- [andreataide86 ClawHub profile](https://clawhub.ai/user/andreataide86) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Markdown instructions with client-facing text, JSON/JSONL records, and local mission files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates an eight-stage business workflow and records mission, ledger, revenue, dashboard, and client-profile data under ~/.cashclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
