## Description:

Acts as a chief financial officer advisor for cash forecasting, runway and burn analysis, monthly close, fundraising models, board reporting, capital structure, revenue definitions, tax exposure triage, and acquisition readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, operators, and finance teams use this skill to reason through CFO-level decisions such as runway, hiring and cuts, fundraising, debt, board materials, revenue recognition, tax escalation, international expansion, and M&A preparation. It provides advisory guidance and draft finance artifacts while leaving regulated, irreversible, or approval-heavy decisions to humans and licensed professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CFO memory or preference files could contain sensitive finance, employee, customer, tax, or banking details if users store more than context and preferences.

Mitigation: Use ~/Clawic/data/cfo/ only for preferences and high-level context; do not store credentials, account numbers, tax IDs, raw bank or payroll exports, or sensitive employee/customer detail.

Risk: Financial guidance can affect cash, fundraising, debt, tax, audit, compensation, or deal decisions if treated as an automated decision maker.

Mitigation: Use the skill as advisory support only; route regulated, irreversible, approval-heavy, tax, audit, legal, payment, and money-movement decisions to humans and licensed professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/cfo)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic CFO skill homepage](https://clawic.com/skills/cfo)
- [Security and privacy guidance](artifact/SKILL.md#security--privacy)
- [Setup and local memory guidance](artifact/setup.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown advisory responses, structured finance checklists, tables, formulas, and local configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or maintain local preference and context files under ~/Clawic/data/cfo/ when the user provides preferences; does not execute code, call external services, connect to financial accounts, or move money.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
