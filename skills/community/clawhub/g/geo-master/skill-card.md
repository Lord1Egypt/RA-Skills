## Description:

品牌AI可见性监控Skill。自动搜索Kimi/讯飞星火/文心一言/智谱等AI平台，检测品牌关键词可见性，生成0-100 GEM评分，AI分析"为什么没被推荐"，支持飞书推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, and growth teams use this skill to check whether selected brand names appear in AI search or assistant responses, compare coverage across supported platforms, calculate a GEM visibility score, and receive concise optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand and competitor terms may be sent to third-party AI or search services and to a configured Feishu webhook.

Mitigation: Use non-sensitive inputs where possible, review configured endpoints before running scans, and avoid enabling Feishu delivery for confidential reports.

Risk: The included API service contains shared placeholder credentials and an embedded Tavily key fallback.

Mitigation: Do not deploy the API service as-is; remove embedded credentials, rotate any exposed keys, and configure secrets through managed environment variables.

Risk: Paid/API platform coverage and entitlement behavior may be overstated relative to the included checks.

Mitigation: Confirm platform coverage, entitlement checks, and rate limits before relying on paid-tier reports or exposing the service to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiji0802/skills/geo-master)
- [Publisher profile](https://clawhub.ai/user/qiji0802)
- [YK-Global website](https://yk-global.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown reports, and optional Feishu notification cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include per-platform visibility findings, GEM score details, and short optimization recommendations.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
