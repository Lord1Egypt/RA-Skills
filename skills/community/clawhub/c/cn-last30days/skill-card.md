## Description:

研究过去30天中国社媒平台上任何话题的真实讨论，覆盖小红书、抖音、公众号三大平台并返回跨平台舆情综合分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand operators, and market researchers use this skill to investigate recent Chinese social-media topics, compare brand or product reputation, and generate cross-platform sentiment reports from Xiaohongshu, Douyin, and WeChat Official Accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topic queries and related research context may be sent to external services.

Mitigation: Use only non-confidential topics and avoid brand, customer, or investigation terms that should not be shared with WebSearch or RedFox.

Risk: Generated HTML is reported as not safely sanitized and may be opened automatically.

Mitigation: Inspect generated files before opening them, disable or avoid automatic opening where possible, and validate links and escaped content before sharing reports.

Risk: The skill uses a RedFox API key for data access.

Mitigation: Use a revocable API key with appropriate scope, avoid hard-coding it, and monitor where generated reports and logs are saved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/cn-last30days)
- [Output Rules and Templates](artifact/references/output-rules.md)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown research report with tables and links; optional JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses topic keywords, platform selection, item count, day range, output format, output directory, and an optional REDFOX_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
