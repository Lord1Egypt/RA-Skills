## Description: <br>
AI-powered financial tracking for solopreneurs \u2014 log income and expenses, monitor revenue toward monthly goals, generate P&L snapshots, flag cash flow risks, and build a running financial picture with zero spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
External users and solopreneurs use this skill to have an agent maintain local income, expense, target, monthly P&L, cash-flow, and tax-estimate tracking files. The skill supports lightweight business finance operations without requiring a spreadsheet or accounting application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tax estimates and financial summaries may be inaccurate, incomplete, or unsuitable for compliance decisions. <br>
Mitigation: Treat outputs as rough tracking aids, reconcile them against source records, and consult qualified tax, accounting, or legal professionals for binding decisions. <br>
Risk: Finance files can contain sensitive business or personal financial data. <br>
Mitigation: Store only the amounts, vendors, categories, and notes needed for business tracking; do not store account numbers, full payment-card numbers, banking credentials, or other secrets. <br>
Risk: Agent-maintained logs, monthly close summaries, and state files can misclassify entries or drift from source records. <br>
Mitigation: Review income-log, expense-log, finance-state, tax-estimate, and monthly-summary updates before relying on them for business planning. <br>


## Reference(s): <br>
- [Financial Tracker on ClawHub](https://clawhub.ai/Clawdssen/agentledger-financial-tracker) <br>
- [Clawdssen publisher profile](https://clawhub.ai/user/Clawdssen) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, JSON] <br>
**Output Format:** [Markdown finance logs and summaries plus JSON state/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local finance files such as income logs, expense logs, monthly summaries, tax estimates, and finance-state JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
