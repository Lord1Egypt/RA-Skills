## Description:

Query and analyze personal finance data from the Copilot Money Mac app, including spending, transactions, account balances, budgets, and financial trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chardigio](https://clawhub.ai/user/chardigio)

### License/Terms of Use:


## Use Case:

External users with Copilot Money on macOS use this skill to ask an agent questions about local transactions, balances, budgets, recurring expenses, investments, and spending trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and summarize sensitive local financial records from Copilot Money.

Mitigation: Install only when that access is acceptable, ask specific questions, and avoid requests that dump raw database or cache contents.

Risk: Financial answers may depend on local app sync state and available cache contents.

Mitigation: Confirm Copilot Money has synced locally before relying on transaction, budget, balance, or investment summaries.

## Reference(s):

- [Copilot Money](https://copilot.money)
- [ClawHub release page](https://clawhub.ai/chardigio/skills/copilot-money-mac)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, SQL, guidance]

**Output Format:** [Markdown responses with SQL queries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Copilot Money SQLite and Firestore LevelDB data; no external service transmission is described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
