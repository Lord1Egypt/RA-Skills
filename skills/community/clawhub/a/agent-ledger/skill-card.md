## Description:

Track AI agent earnings, tasks, and payments when logging completed work, checking balances, viewing payment history, or preparing invoice records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to record completed work, track pending and paid amounts, store a wallet address, and export local ledger data. It is best treated as a lightweight local tracker rather than a payment processor or accounting system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial metadata and wallet information are stored in plaintext local files.

Mitigation: Use the skill only for low-sensitivity local tracking unless file permissions, backups, and retention practices are appropriate for the records being stored.

Risk: Input-validation flaws could corrupt or misrepresent ledger data.

Mitigation: Review ledger entries and exported JSON or CSV before using them for client records, invoices, or reconciliation.

Risk: The description overstates payment and invoicing support.

Mitigation: Treat the skill as a local earnings tracker, not as a payment processor, reliable invoicing system, or formal accounting tool.

## Reference(s):

- [Agent Ledger on ClawHub](https://clawhub.ai/rogue-agent1/skills/agent-ledger)
- [Publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON or CSV ledger export output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSONL ledger entries and JSON configuration under ~/.agent-ledger by default, or AGENT_LEDGER_DIR when set.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
