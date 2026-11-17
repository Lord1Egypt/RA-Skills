## Description:

抖音每日点赞飙升榜查询工具。日度收录全平台抖音作品，输出单日新增点赞TOP50榜单，支持按赛道分类查询、历史日期回溯（最多30天）。当用户查询抖音飙升榜、抖音点赞飙升、抖音飙升排名、抖音飙升榜时使用。触发词：抖音飙升榜、点赞飙升、飙升排名、飙升榜、抖音飙升、抖音新增。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, short-video creators, MCN agencies, and data analysts use this skill to query Douyin works with the largest single-day like increases, filter by content category, and review recent historical trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends Douyin ranking query parameters to redfox.hk.

Mitigation: Configure REDFOX_API_KEY only from the documented RedFox source, treat it as a secret, and review key scope, expiry, and revocation options before use.

Risk: Generated ranking entries can include video links returned by the external API.

Mitigation: Review links before opening them and avoid treating returned URLs as independently verified by the skill.

Risk: The advertised subscription or auto-push behavior is not enough by itself to prove a scheduler, cancellation path, or confirmation flow.

Mitigation: Rely on subscription behavior only when the publisher provides operational documentation for scheduling, user confirmation, and cancellation.

## Reference(s):

- [API configuration](references/api-config.md)
- [Interaction guide](references/interaction-guide.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox hot content rank API](https://redfox.hk/story/api/dy/search/hotContentRank)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-content-surge)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables with clickable work links, plus concise setup and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to TOP20 results; can return up to TOP50 per category and supports dates within the documented 30-day lookback window.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
