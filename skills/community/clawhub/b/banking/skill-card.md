## Description:

Manage retail and business banking workflows with payment operations, account controls, reconciliation, fraud response, and compliant communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees and operations teams use this skill to structure retail and business banking workflows for onboarding, payments, reconciliation, fraud incidents, and customer-safe communications. It helps classify requests, collect jurisdiction and account context, confirm controls, and escalate compliance-sensitive cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local banking notes may capture sensitive banking context if used carelessly.

Mitigation: Keep notes under ~/banking/ limited to operational controls, status, decisions, and non-sensitive context; do not store customer secrets, full account numbers, credentials, or regulated personal data.

Risk: Banking workflow guidance could be mistaken for legal advice or authorization to execute financial actions.

Mitigation: Use the skill as an operational checklist and escalation aid; route legal determinations, KYC, AML, sanctions issues, and irreversible fund movement to qualified owners with documented approvals.

Risk: Payment guidance without verified controls can increase fraud or operational loss risk.

Mitigation: Confirm sender authority, beneficiary validation, amount, cutoff timing, approvals, and rollback or recall paths before giving execution steps.

## Reference(s):

- [ClawHub Banking Skill](https://clawhub.ai/ivangdavila/skills/banking)
- [Banking Skill Homepage](https://clawic.com/skills/banking)
- [Setup - Banking](artifact/setup.md)
- [Banking Intake Checklist](artifact/intake-checklist.md)
- [Payment Operations Guide](artifact/payment-ops.md)
- [Banking Incident Response](artifact/incident-response.md)
- [Customer Messaging Patterns](artifact/customer-messaging.md)
- [Compliance Scope Boundaries](artifact/compliance-scope.md)
- [Memory Template - Banking](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, checklists, communication templates, and local memory file structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain concise local operational notes under ~/banking/ when the agent uses the memory template.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
