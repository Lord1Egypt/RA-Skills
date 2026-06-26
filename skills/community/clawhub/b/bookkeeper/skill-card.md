## Description: <br>
Automates invoice intake from Gmail, extracts invoice data with OCR, verifies payment in Stripe, and creates reconciliation-ready accounting entries in Xero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business operators, finance teams, and developers use this skill to automate preparatory bookkeeping for emailed invoices while preserving review gates before accounting records are posted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive email, invoice, payment, and accounting data. <br>
Mitigation: Use it only with clear approval, protect API keys, and keep mailbox searches narrow to the intended invoices. <br>
Risk: Incorrect OCR extraction or ambiguous payment matching could lead to inaccurate accounting records. <br>
Mitigation: Require manual review when critical fields have uncertainty flags, payment matches are ambiguous, or quality gates fail. <br>
Risk: Automated accounting writes can create duplicate or incorrect records if run without controls. <br>
Mitigation: Require an explicit posting policy, preserve idempotency keys, and avoid marking records as paid without payment evidence. <br>


## Reference(s): <br>
- [Bookkeeper ClawHub page](https://clawhub.ai/h4gen/bookkeeper) <br>
- [Publisher profile](https://clawhub.ai/user/h4gen) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with structured sections and inline JSON or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns IntakeSummary, ExtractionSummary, PaymentVerification, AccountingAction, and ReviewQueue; routes uncertain records to manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
