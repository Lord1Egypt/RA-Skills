## Description:

Query Copilot Money personal finance data (accounts, transactions, net worth, holdings, asset allocation) and refresh bank connections. Use when the user asks about finances, account balances, recent transactions, net worth, investment allocation, or wants to sync/refresh bank data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayhickey](https://clawhub.ai/user/jayhickey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent query Copilot Money through an unofficial CLI for account balances, transactions, net worth, holdings, allocation, and bank-connection refresh workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned unofficial CLI that handles sensitive financial data.

Mitigation: Install only after verifying the copilot-money-cli package source and version, preferably in an isolated Python environment.

Risk: Browser auto-detection can read Copilot Money session tokens from local browser storage.

Mitigation: Avoid auto-detection unless needed, use manual token entry when appropriate, and know how to revoke the Copilot Money session token.

## Reference(s):

- [Copilot Money](https://copilot.money)
- [ClawHub Copilot Money Skill](https://clawhub.ai/jayhickey/skills/copilot-money)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation, authentication, Copilot Money CLI commands, and interpretation of returned personal finance data.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
