## Description: <br>
Turns an AI agent into a local-first personal finance assistant for logging transactions, enforcing budgets, managing savings goals, and producing financial reports through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill with an AI agent to track personal expenses and income, enforce category budgets, manage recurring transactions and savings goals, and request weekly, monthly, or year-to-date financial summaries. It is intended for local workspace use with user-managed financial JSON and CSV files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates local JSON and CSV files containing private financial records. <br>
Mitigation: Install only in a workspace you control, keep ledgers out of shared or public repositories, and manage backups as sensitive financial data. <br>
Risk: Natural-language transaction parsing, recurring rules, and budget reports can be incorrect or incomplete. <br>
Mitigation: Review parsed transactions, recurring rules, and generated reports before relying on them for financial decisions. <br>
Risk: Foreign-currency handling can require exchange-rate data that may conflict with the stated no-external-API privacy model. <br>
Mitigation: Use manually supplied exchange rates when preserving local-only operation is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-budget-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/1kalin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON and CSV examples, file-edit guidance, and occasional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local budget profile, ledger, goals, recurring-rules, and CSV export files when directed by the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
