## Description:

BillClaw helps agents operate a local Python and SQLite bookkeeping assistant for adding, querying, deleting after confirmation, categorizing, reporting, CSV export, and launching a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520mianxiangduixiang520](https://clawhub.ai/user/520mianxiangduixiang520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a local personal ledger, review transactions, create financial summaries and charts, export CSV data, and open a local dashboard while preserving confirmation steps for destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages private financial records in a local SQLite ledger.

Mitigation: Install only when local financial record management is acceptable, and keep the database path and generated outputs under user-controlled storage.

Risk: The local dashboard and CSV export can expose sensitive transaction data.

Mitigation: Keep the dashboard bound to 127.0.0.1, avoid untrusted transaction data, and review CSV destination paths before export.

Risk: Delete and category-merge operations can permanently change ledger records.

Mitigation: Use the documented preview commands first and execute confirm commands only after the user explicitly approves the affected records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/520mianxiangduixiang520/skills/bill-claw)
- [Setup guide](SETUP.md)
- [Bundled dashboard dependency notes](scripts/static/vendor/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Concise text or Markdown with CLI commands, JSON-backed results, report image paths, and CSV file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local SQLite updates, PNG report charts, CSV exports, and localhost dashboard guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
