## Description: <br>
Query and analyze personal finance data from the Copilot Money Mac app, including spending, transactions, account balances, budgets, and financial trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chardigio](https://clawhub.ai/user/chardigio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with Copilot Money on macOS use this skill to ask an agent focused questions about locally stored personal finance records, such as spending trends, transactions, balances, budgets, recurring payments, and investments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive personal financial records to the agent session. <br>
Mitigation: Ask narrow, date-limited questions, prefer scoped SELECT queries, avoid full table dumps, and treat returned data as sensitive financial information. <br>


## Reference(s): <br>
- [Copilot Money](https://copilot.money) <br>
- [ClawHub Skill Page](https://clawhub.ai/chardigio/copilot-money-mac) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local query guidance and analysis over Copilot Money SQLite and Firestore LevelDB cache data; returned financial data should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
