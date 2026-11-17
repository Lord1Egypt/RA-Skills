## Description:

支持发送和查询钉钉日报/周报，可对工作质量总结与评分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigint1](https://clawhub.ai/user/bigint1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace agents use this skill to create, send, query, and summarize DingTalk daily or weekly reports. It can retrieve report templates, submit Markdown report content, search employee IDs by name, and produce work-quality summaries and scores from queried reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses enterprise DingTalk credentials to access sensitive workplace reports and employee lookup data.

Mitigation: Install only after enterprise review, use a least-privilege DingTalk internal app, and restrict report query or employee search workflows to authorized users.

Risk: Running the authentication script directly can print a live access token.

Mitigation: Avoid running scripts/auth.js directly and prevent access tokens from being exposed in logs, chat transcripts, or shared outputs.

Risk: Report submission can send workplace content to selected users or chats.

Mitigation: Confirm recipients, group targets, and chat notification settings before sending a report.

## Reference(s):

- [DingTalk report API specification](references/api-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DingTalk API credentials to retrieve templates, create or query reports, and search employee IDs.]

## Skill Version(s):

0.9.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
