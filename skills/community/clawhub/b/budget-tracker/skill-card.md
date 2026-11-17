## Description:

Budget Tracker helps agents record local income and expense entries, list recent transactions, and produce simple financial summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to keep a simple local ledger for personal expenses, project costs, or monthly spending review. It is best treated as a lightweight local tracker rather than a full budgeting, export, or multi-currency finance system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive ledger entries and notes are stored in plaintext under $HOME/.budget-tracker.

Mitigation: Restrict permissions on $HOME/.budget-tracker and avoid entering sensitive notes unless plaintext local storage is acceptable.

Risk: The release overstates finance capabilities such as reliable multi-currency support, budgeting, monthly reporting, or export workflows.

Mitigation: Use it only as a simple local ledger and review generated summaries before relying on them for accounting or financial decisions.

## Reference(s):

- [ClawHub Budget Tracker Skill Page](https://clawhub.ai/ckchzh/skills/budget-tracker)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a plaintext local JSON ledger at $HOME/.budget-tracker/ledger.json when the shell script is run.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
