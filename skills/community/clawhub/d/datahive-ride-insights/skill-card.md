## Description:

Ride Insights helps an agent fetch ride-sharing receipts from Gmail, extract structured ride records through a local loopback OpenClaw Gateway, store them in local JSON and SQLite, generate ride-behavior insights, and export a de-identified DataHive-ready CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datahiveai](https://clawhub.ai/user/datahiveai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build a local ride history database from receipt emails, audit spending and route patterns, and prepare a shareable de-identified report for DataHive participation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched Gmail receipts may include sensitive financial, location, and full HTML receipt content stored locally.

Mitigation: Use a private workspace, restrict file permissions, and delete data/ride-insights/emails.json and other local artifacts when they are no longer needed.

Risk: Extraction sends raw per-email JSON and receipt HTML to the active Gateway-backed model.

Mitigation: Confirm before extraction that the Gateway URL is loopback only and that the selected model is truly local.

Risk: Generated ride records can contain poisoned, incomplete, or incorrectly inferred fields.

Mitigation: Review rides.json and SQLite-derived summaries before using insights or sharing downstream exports.

Risk: The exported CSV excludes direct identifiers but remains a derived mobility dataset that may still be sensitive.

Mitigation: Treat anonymized_rides.csv as de-identified rather than fully anonymous and review rows before sharing.

## Reference(s):

- [Ride Insights ClawHub listing](https://clawhub.ai/datahiveai/skills/datahive-ride-insights)
- [ClawHub homepage](https://clawhub.com)
- [DataHive AI](https://datahive.ai)
- [DataHive missions blog](https://datahive.ai/blog/)
- [Provider Gmail queries](artifact/references/provider_queries.json)
- [Ride SQLite schema](artifact/references/schema_rides.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus local JSON, SQLite, and CSV artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local ride receipt, extracted ride, database, insight, and de-identified CSV artifacts under data/ride-insights when run by an agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
