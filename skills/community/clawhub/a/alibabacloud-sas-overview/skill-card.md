## Description:

Queries Alibaba Cloud Security Center overview data, including security posture, asset status, risk governance, asset trends, and billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to retrieve requested Security Center posture, asset, operations, trend, or billing data from Alibaba Cloud accounts. It reports overview data and does not remediate findings or change cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a downloaded CLI installer and update CLI plugins, including plugins unrelated to the requested query.

Mitigation: Review setup before execution; use an isolated CLI environment with approved, verified dependencies; require approval for installation, persistent settings changes, and plugin updates.

Risk: Cloud queries require credentials and may access security and account data.

Mitigation: Use a read-only cloud identity limited to the requested services, and keep credentials out of chat.

## Reference(s):

- [Alibaba Cloud Security Center DescribeVersionConfig API](https://help.aliyun.com/zh/security-center/developer-reference/api-sas-2018-12-03-describeversionconfig)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured JSON query data with a concise Markdown or text summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-aware; may report partial or unavailable modules when permissions, regions, or service capabilities limit results.]

## Skill Version(s):

0.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
