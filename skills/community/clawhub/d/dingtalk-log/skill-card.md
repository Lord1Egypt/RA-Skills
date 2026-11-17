## Description:

dingtalk-log helps agents guide authorized DingTalk enterprise app users through querying employee log reports with the topapi/report/list API by time range, template name, or employee user ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdsw](https://clawhub.ai/user/3rdsw)

### License/Terms of Use:


## Use Case:

Developers and enterprise administrators use this skill to construct DingTalk report-list requests, handle pagination, and parse returned employee log data when they are authorized to access the relevant organization's reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill concerns access to sensitive employee report data.

Mitigation: Use it only with authorization for the relevant organization and apply narrow user, template, and time filters.

Risk: Access tokens and report results may expose business or personal information if retained unnecessarily.

Mitigation: Avoid storing access tokens or report contents longer than necessary and cache tokens only for their intended validity window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3rdsw/skills/dingtalk-log)
- [DingTalk OAuth access token endpoint](https://api.dingtalk.com/v1.0/oauth2/accessToken)
- [DingTalk report list API endpoint](https://oapi.dingtalk.com/topapi/report/list)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes access-token handling, request-parameter constraints, pagination flow, response parsing, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
