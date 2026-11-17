## Description:

查询抖音作品七日新增点赞榜，支持按赛道筛选、回溯最多30天的榜单，并在积分不足时提供支付宝充值后续查流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users can discover Douyin videos with the strongest seven-day increase in likes, filter results by content category, and review recent historical rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recharge flow may install payment software and initiate an Alipay payment when API credits are insufficient.

Mitigation: Require approval for payment-tool installation and each recharge; use a reviewed fixed package version, and verify the merchant and amount in Alipay before paying.

Risk: The ranking API receives the configured RedFox API key and query parameters.

Mitigation: Store the API key in a protected secret or environment variable, and send it only to the documented RedFox ranking API.

## Reference(s):

- [API configuration](references/api-config.md)
- [Interaction guide](references/interaction-guide.md)
- [Alipay recharge guidance](references/alipay-recharge.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox ranking API](https://redfox.hk/story/api/dy/search/hotContentRank)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown ranking list with linked video titles]

**Output Parameters:** [Up to 50 ranked results per category and date]

**Other Properties Related to Output:** [Supports category filtering and historical queries within the documented 30-day range.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
