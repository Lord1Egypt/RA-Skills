## Description:

抖音每日最热作品榜查询工具，日度收录全平台抖音作品并输出单日点赞 TOP50 榜单，支持赛道分类查询、最多 30 天历史回溯和订阅推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content operations teams, creators, brands, MCNs, and data analysts use this skill to query Douyin daily popularity rankings, filter by category, review recent historical trends, and request Markdown tables with links to original works.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and performs outbound ranking lookups against RedFox services.

Mitigation: Install only when RedFox is trusted with the API key; confirm key scope, expiry, and revocation support before use.

Risk: Subscription and push behavior is advertised without detailed opt-in, cancellation, storage, or scheduler documentation.

Mitigation: Treat subscription use as under-specified until the publisher documents explicit consent, cancellation, retention, and scheduling behavior.

Risk: Remote API data is rendered as clickable Markdown links to Douyin works.

Mitigation: Review links before opening and avoid treating returned titles or URLs as trusted content.

## Reference(s):

- [API configuration](references/api-config.md)
- [Interaction guide](references/interaction-guide.md)
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/douyin-daily-hot-redfox)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown tables and concise explanatory text, with optional shell commands for API key setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to the top 20 ranking rows and can output up to 50 rows when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
