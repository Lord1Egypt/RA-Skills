## Description:

抖音七日点赞飙升榜查询工具，按全平台或赛道输出七日新增点赞 TOP50，并支持最多 30 天历史回溯。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, short-video creators, MCN teams, and data analysts use this skill to discover weekly Douyin content surges, compare category trends, review recent history, and request daily ranking pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API-key-backed ranking queries to RedFoxHub.

Mitigation: Use a scoped, revocable API key and install the skill only when you trust RedFoxHub with those queries.

Risk: Remote API content is rendered as clickable Markdown links.

Mitigation: Review links before opening them and avoid using the skill where unvalidated external links are unsuitable.

Risk: Subscription or daily push behavior is described without clear consent, storage, cancellation, or delivery controls.

Mitigation: Do not enable scheduled delivery until those controls are documented and acceptable for the deployment.

## Reference(s):

- [API 配置说明](references/api-config.md)
- [交互逻辑与示例](references/interaction-guide.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub hot content rank endpoint](https://redfox.hk/story/api/dy/search/hotContentRank)
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/douyin-weekly-surge-redfox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown ranking tables with clickable video links and concise status or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to TOP20 results and can present up to TOP50 results per category; requires REDFOX_API_KEY for live API queries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
