## Description: <br>
Process personal/work expenses and reimbursement claims in a structured, low-friction workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austineyapp](https://clawhub.ai/user/austineyapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operators use this skill to organize receipts, categorize spend, identify blocked reimbursement items, calculate totals, and prepare claim summaries, notes, and follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipts, policies, and claim details may contain sensitive personal or business information. <br>
Mitigation: Provide only receipts, policies, and claim details you are comfortable sharing with the agent, and redact unnecessary sensitive details before use. <br>
Risk: Generated claim summaries, totals, or approval drafts may be incomplete or misleading if inputs are missing or extracted incorrectly. <br>
Mitigation: Review generated summaries, totals, blocked-item reasons, and draft messages before submitting them to an expense system or approver. <br>


## Reference(s): <br>
- [Expense Item Schema](references/expense-schema.md) <br>
- [Claim Templates](references/claim-templates.md) <br>
- [Ops Cadence](references/ops-cadence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise Ready, Blocked, and Next action sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes claim-ready items, blocked-item fixes, totals by category and currency, missing-document count, and draft approval or follow-up copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
