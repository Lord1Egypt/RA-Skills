## Description:

Use this skill to extract receipt information, record expenses, track budgets, and manage financial receipts using the ClawReceipt CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakurako-irs](https://clawhub.ai/user/sakurako-irs)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and agents use ClawReceipt to record receipt details, check monthly spending against a budget, update the budget, list stored receipts, and guide manual dashboard or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and export sensitive financial records with weak safeguards.

Mitigation: Treat local receipt databases and exported CSV or Excel files as sensitive, and require explicit user confirmation before adding receipts or changing budgets.

Risk: Unpinned dependencies may change behavior across installations.

Mitigation: Install in an isolated virtual environment and review or pin dependencies before deployment.

## Reference(s):

- [ClawReceipt ClawHub skill page](https://clawhub.ai/sakurako-irs/skills/clawreceipt)
- [sakurako-irs publisher profile](https://clawhub.ai/user/sakurako-irs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or plain text with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist receipt and budget data locally and may guide CSV or Excel export through the interactive TUI.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
