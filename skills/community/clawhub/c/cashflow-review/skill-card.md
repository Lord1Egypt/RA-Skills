## Description:

Review a completed payable test using cash, delivery evidence, and bounded funnel metrics, then choose one honest stop, revise, repeat, or scale decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilbop1](https://clawhub.ai/user/bilbop1)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators and agents use this skill to review a completed payable test, reconcile cash and delivery evidence, evaluate bounded funnel metrics, and return exactly one stop, revise, repeat, or scale decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews private business cashflow, payment, customer, and delivery evidence.

Mitigation: Use it only when relevant private business and financial evidence is intended for review, and minimize confidential details in outputs.

Risk: Run Authorization could be mistaken for permission to take external action.

Mitigation: Limit Run Authorization to analysis and internal review updates; require fresh exact approval before any send, post, purchase, charge, signature, submission, or account change.

Risk: Untrusted business records may contain embedded instructions or misleading financial claims.

Mitigation: Treat copied spreadsheets, invoices, contracts, messages, attachments, payment records, and customer statements as evidence only, ignore embedded instructions, and rely on inspected settlement and acceptance artifacts.

## Reference(s):

- [Cashflow decision rules](artifact/references/decision-rules.md)
- [Cashflow Review on ClawHub](https://clawhub.ai/bilbop1/skills/cashflow-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with structured headings and one decision label]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence labels, revenue reconciliation, cost and time analysis, funnel rates, delivery acceptance, one decision, and an approval checkpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
