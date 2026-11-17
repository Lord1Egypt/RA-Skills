## Description:

Queries Upkuajing customs data for U.S. import statistics by state or city, including import record counts, container counts, recent 90-day activity, and cursor pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, logistics analysts, and market researchers use this skill to monitor U.S. import activity and compare state-level or city-level import distribution. It supports market-entry and logistics analysis using customs import statistics from the Upkuajing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls and recharge-order helpers can spend or prepare spending from the user's account balance.

Mitigation: Tell the user when an action may incur cost, check current pricing through the documented pricing source, and wait for explicit confirmation in a separate user message before running paid calls or creating recharge orders.

Risk: The skill can read and store UPKUAJING_API_KEY in a local ~/.upkuajing/.env file.

Mitigation: Prefer managed secret storage or restrictive local file permissions, and verify only that the key exists without printing or pasting the file contents.

Risk: Error reports may include request context or response details that reveal sensitive operational information.

Mitigation: Review and minimize error-report context before submission, and submit reports only after the user confirms.

## Reference(s):

- [国家贸易概览-美国进口交易 API 参考](references/customs-overview-us-import-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-us-import-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid API calls can return fee and requestId metadata.]

## Skill Version(s):

1.0.1 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
