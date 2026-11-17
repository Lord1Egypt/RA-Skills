## Description:

7-day weather forecast query powered by Alibaba Cloud IQS web search and page reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query 7-day weather forecasts for a city through Alibaba Cloud IQS. It returns structured forecast JSON for supported weather sites and raw text with extraction guidance when a page cannot be parsed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send city queries and selected page URLs to Alibaba Cloud IQS.

Mitigation: Use the skill only when this external data sharing is acceptable for the user and deployment context.

Risk: The artifact encourages agents to add parser code after reading raw webpage content from unknown sites.

Mitigation: Treat raw webpage content as untrusted data and require explicit human review before modifying scripts/weather.mjs or registering new parsers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-iqs-weather-query)
- [Alibaba Cloud IQS Search Skill](https://skills.aliyun.com/skills/alibabacloud-iqs-search)
- [Alibaba Cloud IQS API Key Documentation](https://help.aliyun.com/zh/document_detail/3025781.html)
- [Alibaba Cloud IQS UnifiedSearch Documentation](https://help.aliyun.com/zh/document_detail/2883041.html)
- [Alibaba Cloud IQS ReadPageBasic Documentation](https://help.aliyun.com/zh/document_detail/2983380.html)

## Skill Output:

**Output Type(s):** [json, text, shell commands, configuration, guidance, code]

**Output Format:** [JSON weather forecast data or raw page text with agent guidance; documentation includes Markdown and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY and Node.js 18 or newer; forecast output is limited to up to 7 days.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
