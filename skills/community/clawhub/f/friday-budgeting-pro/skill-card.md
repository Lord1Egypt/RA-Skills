## Description:

Friday Budgeting Pro is an AI-powered personal finance tracker that connects to banks through Plaid, auto-classifies transactions, syncs daily, exports to Excel, and supports personal, rental property, and investment ledgers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riddy21](https://clawhub.ai/user/riddy21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent skill to manage local personal finances through an MCP-enabled assistant: connect banks, sync and classify transactions, review uncertain items, manage ledgers, and export reports.

### Deployment Geography for Use:

Canada

## Known Risks and Mitigations:

Risk: The skill handles bank transaction data, Plaid credentials, OpenClaw credential files, and LLM provider access through a persistent local daemon.

Mitigation: Install only on a trusted macOS profile after reviewing the requested access and accepting local credential and transaction handling.

Risk: LLM classification fallback can use configured external provider credentials for transaction classification.

Mitigation: Confirm the configured LLM path before syncing financial data, and review uncertain classifications before relying on reports.

Risk: Installation performs Python package changes, database initialization, and launchd daemon registration.

Mitigation: Review install hooks before deployment and use the provided uninstall path if the persistent daemon should be removed.

## Reference(s):

- [Friday Budgeting Pro ClawHub Listing](https://clawhub.ai/riddy21/skills/friday-budgeting-pro)
- [Publisher Profile](https://clawhub.ai/user/riddy21)
- [Project Homepage](https://github.com/Riddy21/Friday_Budgeting_Pro)
- [README](README.md)
- [Architecture](ARCHITECTURE.md)
- [Skill Definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses, MCP tool calls, local URLs, and Excel export links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local daemon actions, Plaid connection flows, transaction classification, and Excel workbook generation.]

## Skill Version(s):

1.0.7 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
