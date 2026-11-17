## Description:

Summarize what a user did on macOS, Windows, or Linux using local ActivityWatch records, with privacy-preserving live-state and Screen Time fallbacks when records are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyewang](https://clawhub.ai/user/liuyewang)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to summarize local computer activity from ActivityWatch into daily or weekly app, timeline, project, billable, and spreadsheet-ready reports while keeping activity data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive local activity records, including app names and sanitized window titles.

Mitigation: Grant access only when local activity reporting is intended, keep reports local, and avoid exporting or sharing activity data unless explicitly requested.

Risk: The helper accepts a configurable ActivityWatch API URL while processing sensitive activity data.

Mitigation: Use 127.0.0.1 or another verified loopback-only ActivityWatch endpoint, and do not use remote --api-url values.

Risk: Saved exports and project or billable rules can reveal work patterns or client metadata.

Mitigation: Create exports and apply local rules only after an explicit request, and review saved files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyewang/skills/computer-usage-summary)
- [Publisher profile](https://clawhub.ai/user/liuyewang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON, TSV, and CSV tables, with shell commands and local configuration guidance when setup or exports are requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet-safe escaping; optional local file export only when explicitly requested]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
