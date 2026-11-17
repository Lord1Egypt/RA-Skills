## Description:

Queries and analyzes DingTalk attendance clock-in data, including lateness, early departure, absenteeism, attendance rate, missed clock-ins, and related workplace attendance questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golden-pigeon](https://clawhub.ai/user/golden-pigeon)

### License/Terms of Use:

MIT-0

## Use Case:

HR, operations, and authorized attendance administrators use this skill to query DingTalk attendance data, review exceptions, and summarize patterns across employees and time ranges. It helps convert natural-language date requests into script arguments, retrieve current or cached attendance records, and produce concise Chinese-language attendance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores identifiable employee attendance history locally in SQLite without clear retention, deletion, or access controls.

Mitigation: Use only with authorized HR or attendance-admin credentials, restrict access to the cache database, define a retention policy, and provide a purge or no-history workflow before routine workplace use.

Risk: Attendance data can expose sensitive workplace behavior and may be misused if queried outside an authorized business purpose.

Mitigation: Scope DingTalk permissions to the minimum needed, verify that each query is authorized, and limit report sharing to users with a legitimate need to know.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golden-pigeon/skills/dingtalk-attendance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Analysis]

**Output Format:** [Structured Chinese Markdown with inline shell commands and attendance summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on DingTalk API responses and local SQLite history for comparison across date ranges.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
