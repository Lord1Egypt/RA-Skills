## Description:

AgentLedger helps AI agents log purchases, manage budgets, generate spending reports, track multi-currency expenses, import Privacy.com card data, and export locally stored ledger data to CSV or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-goro](https://clawhub.ai/user/c-goro)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agent operators use AgentLedger to maintain a local financial audit trail for agent purchases, API costs, subscriptions, infrastructure spend, and budget checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export command can write sensitive ledger data to an unrestricted caller-supplied path and overwrite local files.

Mitigation: Use only explicit, trusted relative export filenames, avoid absolute paths and ../ traversal, and review the destination before exporting ledger data.

Risk: CSV exports may be unsafe when opened in spreadsheet software until export path constraints and CSV escaping are fixed.

Mitigation: Treat CSV exports as untrusted, inspect or escape spreadsheet formulas before opening them, and prefer JSON exports when spreadsheet processing is unnecessary.

Risk: Ledger fields can contain sensitive payment context if agents store card numbers, passwords, or overly detailed receipt information.

Mitigation: Store account aliases and receipt links only, and do not place card numbers or passwords in ledger fields.

## Reference(s):

- [AgentLedger README](README.md)
- [AgentLedger Agent Instructions](SKILL.md)
- [OpenClaw Documentation](https://openclaw.ai)
- [Privacy.com](https://privacy.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JavaScript snippets, shell commands, and local JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores transactions, accounts, budgets, and settings under workspace/ledger; exports selected ledger data as CSV or JSON.]

## Skill Version(s):

1.1.1 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
