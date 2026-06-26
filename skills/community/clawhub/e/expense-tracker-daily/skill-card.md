## Description: <br>
Expense Tracker Daily helps an agent record, query, delete, and summarize local expense entries from natural-language spending requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glorysunshine](https://clawhub.ai/user/glorysunshine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using OpenClaw can ask an agent to record daily spending, classify expenses, list recent entries, delete confirmed records, and summarize spending by day, week, or month. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense descriptions and spending records may contain sensitive personal financial information. <br>
Mitigation: Keep records local, avoid sharing the data file unnecessarily, and review outputs before exposing them to other tools or people. <br>
Risk: Deleting an expense entry removes it from the local JSON record store. <br>
Mitigation: List entries and confirm the target id with the user before running a delete command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glorysunshine/expense-tracker-daily) <br>
- [Category keyword reference](artifact/references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown responses with local Python CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expense records are stored locally under ~/.qclaw/workspace/expense-tracker-data/expenses.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
