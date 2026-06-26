## Description: <br>
Personal finance assistant for AccountantPriv that queries Hapoalim, Isracard, and Max SQLite databases to answer questions about transactions, expenses, income, merchants, subscriptions, monthly summaries, and spending patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharon8811](https://clawhub.ai/user/sharon8811) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to inspect their own AccountantPriv banking and credit card SQLite databases, locate merchant or subscription charges, summarize monthly finances, and analyze spending or income patterns. The skill is intended for direct personal-finance answers in Hebrew using local financial data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad SQL access to sensitive banking databases can expose detailed financial history. <br>
Mitigation: Use only with the user's own AccountantPriv databases, prefer read-only database copies or read-only SQLite connections, and avoid persisting detailed financial history unless explicitly required. <br>
Risk: Financial account numbers or transaction details may appear in documentation or outputs. <br>
Mitigation: Remove real account numbers and sensitive transaction details before sharing documentation, logs, screenshots, or generated answers outside the user's trusted environment. <br>
Risk: Monthly summaries can double count credit card activity when both bank card bills and individual card transactions are combined. <br>
Mitigation: Follow the artifact guidance to use either aggregate bank card bills or detailed card expenses for a calculation, not both together. <br>


## Reference(s): <br>
- [Database Schemas - AccountantPriv](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/sharon8811/accountant-priv-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and optional JSON or tabular script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Python helpers against SQLite databases and summarize sensitive financial records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
