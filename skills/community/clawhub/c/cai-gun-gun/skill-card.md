## Description: <br>
Cai Gun Gun is a personal finance assistant for quick transaction entry, automatic categorization, account balance management, bill import and export, and spending analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmmg55](https://clawhub.ai/user/gmmg55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill through an agent to record income and expenses, review recent bills and balances, import or export Excel bills, and generate personal finance summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial records are copied into both a local data directory and the skill data directory, which may sync in some agent environments. <br>
Mitigation: Confirm the agent environment's sync behavior before storing real financial data and use CAI_GUN_GUN_DATA_DIR when a specific local storage path is required. <br>
Risk: Imports, deletes, and clear operations can alter or remove financial records. <br>
Mitigation: Export a backup before importing or clearing data, require confirmation for destructive operations, and verify delete targets before running commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown responses with Python CLI commands and local JSON or Excel files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores transaction, account, category, and configuration data locally and copies supported data files into the skill data directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
