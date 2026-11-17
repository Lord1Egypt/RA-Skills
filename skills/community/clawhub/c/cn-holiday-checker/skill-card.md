## Description:

Queries Chinese holidays, work-shift arrangements, and determines whether a date is a workday using local calendar data and weekly fallback rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudecaicai](https://clawhub.ai/user/claudecaicai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer China-focused holiday, adjusted workday, and rest-day questions for a given date. It can also refresh the local ICS calendar data from configured sources when updates are enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic updates contact configured external calendar URLs and replace the local ICS data file.

Mitigation: Review PRIMARY_URL and BACKUP_URL before enabling updates; add size and validation limits before relying on untrusted sources.

Risk: Holiday and workday answers depend on the accuracy and freshness of the local ICS calendar data.

Mitigation: Keep calendar data current and verify high-impact scheduling decisions against official sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudecaicai/skills/cn-holiday-checker)
- [Publisher profile](https://clawhub.ai/user/claudecaicai)
- [Primary Chinese holiday calendar source](https://calendars.icloud.com/holidays/cn_zh.ics)
- [Backup Chinese holiday calendar source](https://raw.githubusercontent.com/lanceliao/china-holidays/master/holidays.ics)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Date responses include the queried date, workday/rest-day status, and matching calendar detail when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
