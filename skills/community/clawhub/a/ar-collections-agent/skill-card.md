## Description:

Automates accounts receivable collections workflows with aging analysis, prioritization, outreach drafts, DSO reporting, payment tracking, and bad debt reserve recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting firms and finance teams use this skill to analyze aged receivables, prioritize collections work, draft approved customer outreach, track payment promises, and prepare AR KPI reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer-facing collection messages or AR reports could contain incorrect invoice details or inappropriate escalation language.

Mitigation: Review all collection messages, invoice details, and AR summaries before sending or presenting them.

Risk: Client AR data could be mixed across engagements or exposed to the wrong client.

Mitigation: Keep each client's AR exports, trackers, and analysis separate throughout the workflow.

Risk: QBO or accounting changes could be made without proper authority.

Mitigation: Require explicit authorization and review before any QBO/accounting change, write-off, or journal-entry execution.

Risk: Collections, legal, or tax boundaries could be exceeded for highly overdue accounts or bad debt deductions.

Mitigation: Escalate legal collection actions to an attorney and route PTIN-backed tax guidance to an authorized tax professional.

## Reference(s):

- [AR KPI Formulas Reference](references/ar-kpi-formulas.md)
- [AR Collections Email Templates](references/email-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Guidance]

**Output Format:** [Markdown tables, CSV schedules, email drafts, KPI summaries, and journal-entry recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; external sends and accounting changes require approval.]

## Skill Version(s):

98.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
