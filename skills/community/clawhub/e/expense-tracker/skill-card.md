## Description: <br>
Track daily expenses in structured monthly markdown files with categories, tags, summaries, and spending-pattern analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aholake](https://clawhub.ai/user/aholake) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to log personal expenses, review monthly summaries, and analyze spending patterns from local markdown expense files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense details may contain sensitive personal financial information stored in local markdown files and duplicated backups under Documents. <br>
Mitigation: Use explicit logging requests, avoid sensitive descriptions, and review or delete the backup folder if Documents is synced or shared. <br>
Risk: The skill writes expense data and backups to local filesystem paths. <br>
Mitigation: Review the target workspace and backup location before deployment, and keep date and month inputs in normal YYYY-MM-DD or YYYY-MM format. <br>


## Reference(s): <br>
- [Expense Categories](references/categories.md) <br>
- [ClawHub skill page](https://clawhub.ai/aholake/expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown expense files, terminal text summaries, and optional JSON monthly summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates monthly expense files under the configured workspace and writes pre-change backups under ~/Documents/expenses_backup.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
