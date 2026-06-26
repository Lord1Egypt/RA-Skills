## Description: <br>
Automates accounts receivable collections workflows for accounting firms and finance teams, including aging analysis, prioritization, outreach drafts, DSO reporting, payment tracking, and bad debt reserve recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance teams and accounting firms use this skill to turn QBO exports, invoice CSVs, direct QBO query results, or pasted invoice data into collection priorities, aging analysis, customer outreach drafts, KPI summaries, and bad debt recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive accounts receivable and customer payment data. <br>
Mitigation: Use client-specific inputs only, avoid mixing client data, and delete any persisted payment promise tracker when it is no longer needed. <br>
Risk: Collection emails or QBO changes could create external financial impact if acted on without review. <br>
Mitigation: Keep QBO access read-only unless write access is deliberately granted, and review every collection email before sending. <br>
Risk: Late-stage collections, legal escalation, tax treatment, and write-off execution can exceed the skill's authority. <br>
Mitigation: Escalate legal action to an attorney, route PTIN-backed tax guidance to an authorized provider, and require authorized reviewer approval before write-offs or high-impact escalation. <br>


## Reference(s): <br>
- [AR KPI Formulas Reference](references/ar-kpi-formulas.md) <br>
- [AR Collections Email Templates](references/email-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/ar-collections-agent) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, csv, guidance, configuration] <br>
**Output Format:** [Markdown tables, CSV tables, email drafts, KPI summaries, journal entry drafts, and follow-up schedules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts and recommendations require human approval before external sending, QBO write actions, legal escalation, tax guidance, or write-off execution.] <br>

## Skill Version(s): <br>
98.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
