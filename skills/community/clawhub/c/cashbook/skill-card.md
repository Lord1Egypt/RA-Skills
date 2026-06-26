## Description: <br>
cashbook is a local-first personal bookkeeping skill for recording expenses, managing accounts and budgets, importing Alipay or WeChat CSV records, and generating weekly or monthly reports from a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenkang-xie](https://clawhub.ai/user/wenkang-xie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use cashbook to keep personal finance records locally, including natural-language and screenshot-based transaction capture, account management, budget checks, CSV imports, and periodic spending reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance records are stored in a local SQLite database on the user's machine. <br>
Mitigation: Install only if local storage is acceptable, protect the local machine and backups, and use the CASHBOOK_DB environment variable if a specific database location is required. <br>
Risk: Natural-language, screenshot, and CSV parsing can create incorrect transaction details. <br>
Mitigation: Show parsed entries to the user before saving and use CSV dry-run mode before importing transaction files. <br>
Risk: The advertised export command is missing in this release. <br>
Mitigation: Do not rely on export support until the command is present; use available query and report commands for review. <br>


## Reference(s): <br>
- [ClawHub cashbook listing](https://clawhub.ai/wenkang-xie/cashbook) <br>
- [Account management reference](references/account.md) <br>
- [Budget management reference](references/budget.md) <br>
- [Data model reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown and terminal-style text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite bookkeeping records and produce weekly or monthly summary reports.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
