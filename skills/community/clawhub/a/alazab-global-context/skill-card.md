## Description:

Analyzes static Daftra CSV backups to inventory and link business records, identify ambiguous relationships, and prepare data for migration without accessing a live account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alazabdev](https://clawhub.ai/user/alazabdev)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and developers use this skill to examine Daftra backup CSVs, reconcile clients, suppliers, invoices, orders, and expenses, and prepare migration or import data while flagging uncertain record matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled and user-provided CSVs may contain sensitive business and contact information.

Mitigation: Keep backups and derived outputs access-controlled; avoid exposing personal or financial data in shared responses.

Risk: Duplicate invoice numbers and unverified relationships can produce incorrect totals or record matches.

Mitigation: Check key uniqueness and reconcile row counts and totals before joining; flag ambiguous or unmatched records for review.

Risk: The documented inspection script and reference files are absent from this release artifact.

Mitigation: Analyze the supplied CSVs directly using read-only tools rather than assuming the documented helpers are available.

## Reference(s):

- [Daftra Backup on ClawHub](https://clawhub.ai/alazabdev/skills/alazab-global-context)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV files]

**Output Format:** [Arabic-language analysis and guidance, with separate CSV output files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original column names and identifiers; analyzes static backups without live account access.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
