## Description: <br>
Cn Expense Tracker is a Chinese personal expense tracking skill for recording spending, reviewing monthly statistics, setting budgets, comparing trends, and exporting local CSV data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage personal expenses in Chinese through local command-line workflows, including adding records, checking monthly reports, setting budgets, comparing trends, listing or deleting entries, and exporting CSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleting an expense record permanently rewrites the local expense data file and renumbers remaining records. <br>
Mitigation: Export or back up ~/.qclaw/workspace/expenses.json before using deletion. <br>
Risk: Expense, budget, and export files are stored locally under ~/.qclaw/workspace and may contain personal financial details. <br>
Mitigation: Protect local workspace files and review expenses_export.csv before sharing or importing it elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-expense-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text, local JSON data, and CSV export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores expenses in ~/.qclaw/workspace/expenses.json, budgets in ~/.qclaw/workspace/budget.json, and CSV exports in ~/.qclaw/workspace/expenses_export.csv.] <br>

## Skill Version(s): <br>
1.2.6 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
