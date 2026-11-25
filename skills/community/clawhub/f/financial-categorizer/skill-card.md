## Description:

Process bank transaction CSV exports (Nordea, ICA), auto-categorize transactions using configurable rules, manage transaction links, and generate analytical database views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT

## Use Case:

Individual finance users and developers can import local bank CSV exports into SQLite, organize transactions with category rules and links, and review balances, spending summaries, recurring payments, and cash flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a high-confidence risk that removing a manual category match may also delete user-created transfer links, affecting financial reports. The scan verdict is suspicious, and inspection was incomplete.

Mitigation: Back up the SQLite database and review transaction links before and after manual-match changes; inspect dry-run results before cleanup or auto-linking.

Risk: Supplying --yes or -y can bypass confirmation prompts for destructive database operations.

Mitigation: Back up the database, use a dry run where available, and bypass prompts only after reviewing the intended changes.

## Reference(s):

- [financial-categorizer on ClawHub](https://clawhub.ai/patello/skills/financial-categorizer)
- [patello on ClawHub](https://clawhub.ai/user/patello)

## Skill Output:

**Output Type(s):** [Text, SQLite database records and analytical views]

**Output Format:** [Terminal text and local SQLite data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates a local finance database; destructive operations provide confirmation prompts and dry-run options where supported.]

## Skill Version(s):

1.17.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
