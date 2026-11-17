## Description:

Process bank transaction CSV exports (Nordea, ICA), auto-categorize transactions using configurable rules, manage transaction links, and generate analytical database views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT

## Use Case:

People managing personal finances use this skill to import bank CSVs, categorize transactions, link transfers and reimbursements, and review spending in a local SQLite database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup, auto-linking, recurring discovery, category deletion, and other mutating commands can change or remove records in the local finance database.

Mitigation: Back up the database first, preview with dry-run options when available, and review changes before using --yes.

## Reference(s):

- [Financial Categorizer on ClawHub](https://clawhub.ai/patello/skills/financial-categorizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with CLI commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on a user-selected local SQLite database.]

## Skill Version(s):

1.16.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
