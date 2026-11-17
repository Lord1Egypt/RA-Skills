## Description:

Generates concise Chinese daily work reports for short drama and AI comic production teams, including workload statistics, dialogue and token usage, content progress, and daily risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevenzhou](https://clawhub.ai/user/elevenzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Short drama and AI comic production teams use this skill to turn session status and daily memory entries into a compact Chinese daily report covering output, progress, completed work, next-day tasks, and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report may include sensitive production notes from recent memory files.

Mitigation: Confirm that memory/YYYY-MM-DD.md and memory/targets.md contain only report-appropriate information, or redact sensitive details before generating the report.

Risk: Daily metrics may be incomplete when session status or memory entries are unavailable.

Mitigation: Use the skill's fallback convention of marking missing values with an em dash instead of leaving fields blank.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elevenzhou/skills/eleven-daily-shortdrama-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown daily report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marks unavailable data with an em dash and highlights unusually high token usage in the risk section.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
