## Description: <br>
Friday Budgeting Pro is an AI-powered personal finance tracker that connects to banks via Plaid, auto-classifies transactions, syncs daily, supports personal, property, and investment ledgers, and exports to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riddy21](https://clawhub.ai/user/riddy21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using OpenClaw or another MCP client use this skill to manage local personal finance workflows: connecting banks, syncing and classifying transactions, reviewing budgets, managing ledgers, and exporting reports. <br>

### Deployment Geography for Use: <br>
Canada for Plaid bank-linking workflows; other local budgeting functions are not geography-restricted by the evidence. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles bank data, Plaid credentials, and local finance records. <br>
Mitigation: Use only on a trusted local machine, avoid sharing secrets in chat unless the full agent path is trusted, and review connected accounts and stored profile data during setup. <br>
Risk: The skill installs a persistent local daemon and registers with OpenClaw. <br>
Mitigation: Confirm the LaunchAgent and OpenClaw registration are expected before installation, and review uninstall cleanup for launchd, OpenClaw configuration, cron files, and local Friday Budgeting Pro data. <br>
Risk: Transaction details may be sent to an external LLM provider through fallback behavior. <br>
Mitigation: Disable or explicitly configure external LLM fallback when local-only processing is required, and review provider settings before syncing real financial data. <br>
Risk: The skill can modify budgeting rules and ledgers, which may affect reports and classifications. <br>
Mitigation: Review proposed classification rules, ledger changes, and uncertain transactions before relying on exported reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/riddy21/friday-budgeting-pro) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Skill Homepage](https://github.com/Riddy21/Friday_Budgeting_Pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with MCP tool calls, setup commands, local URLs, and export links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate local database, Plaid, LLM, notification, and Excel export workflows through configured tools.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
