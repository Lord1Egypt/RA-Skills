## Description: <br>
Finance Tracker helps an agent track personal expenses, income, assets, recurring expenses, savings goals, budgets, multi-currency conversions, and spending insights through a local command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Salen-Project](https://clawhub.ai/user/Salen-Project) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to log personal finance records, review spending, manage recurring items and goals, export transaction data, and summarize budget or portfolio status. It is intended for local finance tracking rather than regulated financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive expense, income, goal, asset, and exchange-rate cache files locally under ~/.finance-tracker. <br>
Mitigation: Use it only on systems where local finance records are acceptable, protect the data directory, and avoid entering account credentials or other secrets as transaction text. <br>
Risk: Commands such as delete, undo, edit, asset removal, goal removal, and recurring process can modify or remove finance records. <br>
Mitigation: Have the agent confirm destructive or automated processing commands before execution and keep backups or exports for records that must be recoverable. <br>
Risk: Currency features may contact external exchange-rate services and cache the returned rates. <br>
Mitigation: Review network use before enabling currency conversion in sensitive environments, or rely on cached or fallback rates when live lookup is not appropriate. <br>


## Reference(s): <br>
- [Finance Tracker ClawHub page](https://clawhub.ai/Salen-Project/finance-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text, CSV, or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local finance records under ~/.finance-tracker; currency features may use cached or live exchange-rate data.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md title; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
