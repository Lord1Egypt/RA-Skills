## Description: <br>
Imports billing files, checks duplicates, queries transactions, shows summaries, records expenses or income, manages budgets, and runs these actions through a local bookkeeping CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lastarla](https://clawhub.ai/user/lastarla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to import local Alipay, WeChat, CSV, or XLSX billing files, inspect duplicate imports, query transaction history, view spending summaries, record individual income or expenses, manage budgets, and start a local dashboard when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local financial files and can add or change bookkeeping records. <br>
Mitigation: Install only when the external bookkeeping CLI is trusted, review inferred imports and natural-language entries, and confirm ambiguous or multi-file operations before execution. <br>
Risk: A database reset can remove existing local bookkeeping data. <br>
Mitigation: Require explicit confirmation before any reset action and clearly state the effect before running it. <br>
Risk: Unsupported or misidentified attachments could lead to failed imports or incorrect bookkeeping actions. <br>
Mitigation: Use original filenames or MIME metadata when available, limit supported imports to CSV and XLSX files, and ask the user to choose when multiple candidate files are present. <br>


## Reference(s): <br>
- [Bookkeeping Skill on ClawHub](https://clawhub.ai/lastarla/bookkeeping-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/lastarla) <br>
- [Project Homepage](https://github.com/lastarla/bookkeeping-agent) <br>
- [Bookkeeping Tool Source](https://github.com/lastarla/bookkeeping-tool.git) <br>
- [Install](references/install.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with CLI command execution results summarized for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON output from the local CLI when available and summarizes transaction, import, duplicate, budget, and reminder results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
