## Description:

Collects public Bilibili video engagement metrics in batches and exports the results as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users can collect public Bilibili video metrics for campaign reporting, content tracking, and performance analysis. The skill accepts video links in batches and returns structured results or a CSV export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the default connection can send account credentials over unencrypted HTTP.

Mitigation: Use a trusted HTTPS endpoint with certificate validation enabled, and do not send account tokens over plain HTTP.

Risk: The security summary reports persistent credential migration, and the skill stores account credentials in a local configuration file.

Mitigation: Protect the local configuration file, use a dedicated account where practical, and review migrated credentials before use.

Risk: The security summary notes extra comment-collection capabilities beyond the stated metrics and CSV purpose.

Mitigation: Review the skill's data scope before use and keep activity limited to the requested public video metrics.

Risk: The security assessment was incomplete, covering 33.3% of components, with partially inspected files and degraded static tool-misuse analysis.

Mitigation: Treat the current assessment as partial and review the full package before use with sensitive credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mystery77777777/skills/b-collect)

## Skill Output:

**Output Type(s):** [JSON, CSV files]

**Output Format:** [JSON task results and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-video titles, identifiers, creator names, and seven public engagement metrics; supports batches of 1–50 video links.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
