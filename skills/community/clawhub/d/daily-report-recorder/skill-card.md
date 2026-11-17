## Description:

Records, refines, and archives daily work updates by generating or updating a Markdown report for the current day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bounding-elk](https://clawhub.ai/user/bounding-elk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn daily work notes, troubleshooting updates, meeting notes, and follow-up plans into standardized internal Markdown reports. It merges multiple same-day updates into one report and keeps the wording concise, factual, and outcome-oriented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided work updates may be persisted in local daily Markdown reports.

Mitigation: Avoid entering confidential details unless /data/reports/daily is an appropriate storage location for that information.

Risk: The optional cron example can trigger recurring report prompts.

Mitigation: Review the schedule and payload before enabling any recurring prompt.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bounding-elk/skills/daily-report-recorder)
- [Publisher Profile](https://clawhub.ai/user/bounding-elk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown daily report with a concise text confirmation and optional bash cron configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates /data/reports/daily/YYYY-MM-DD.md and uses Asia/Shanghai timestamps for recorded items.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
