## Description: <br>
Personal budget management with privacy-first local storage for setting budgets, tracking spending, logging expenses, checking budget status, and managing money by category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manually manage personal budgets, log expenses, monitor category limits, generate spending reports, and recover from overages without connecting to bank accounts or external financial services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Budget, income, merchant, and expense details are stored in local files. <br>
Mitigation: Install only if local storage of these financial details is acceptable, and manage retention and deletion of ~/.openclaw/workspace/memory/budget files deliberately. <br>
Risk: Some helper scripts described in the documentation may be absent from the artifact. <br>
Mitigation: Review available scripts before relying on workflows that delete, export, analyze, or change stored budget records. <br>
Risk: Budget guidance can be mistaken for financial advice. <br>
Mitigation: Use outputs for budget tracking and category reallocation only; consult a qualified financial advisor for financial planning, investment, or tax decisions. <br>


## Reference(s): <br>
- [Budget Setup](references/budget-setup.md) <br>
- [Expense Tracking](references/expense-tracking.md) <br>
- [Budget Alerts & Thresholds](references/alerts.md) <br>
- [Reports & Analysis](references/reports.md) <br>
- [Overage Recovery](references/overage-recovery.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AGIstack/budget-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-style text with inline shell commands and local JSON-backed budget records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores budget, income, merchant, and expense details in local files under ~/.openclaw/workspace/memory/budget.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
