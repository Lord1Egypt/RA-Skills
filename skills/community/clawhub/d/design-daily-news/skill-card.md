## Description:

每日设计与科技资讯聚合 - 从优设读报、36氪、虎嗅自动抓取并筛选最新的设计、AI、产品等行业动态。使用此技能获取最新的设计行业新闻、AI 趋势或每日新闻摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyuvision-max](https://clawhub.ai/user/tianyuvision-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation agents use this skill to collect daily design, AI, product, and technology news from 优设读报, 36氪, and 虎嗅 and format it as a concise digest suitable for WeChat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically publish scraped external content to WeChat.

Mitigation: Confirm scheduled delivery is opt-in and review generated digests before sending to shared channels.

Risk: External titles, summaries, and URLs are formatted into Markdown links without documented sanitization.

Mitigation: Sanitize URLs and Markdown text before delivery, especially when reports are sent to other people.

Risk: The archive helper deletes local news files older than 30 days.

Mitigation: Document the retention behavior or disable cleanup unless users expect local archive deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianyuvision-max/skills/design-daily-news)
- [优设读报](https://www.uisdc.com/news)
- [36氪](https://36kr.com)
- [36氪 RSS feed](https://36kr.com/feed)
- [虎嗅](https://www.huxiu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown news digest with numbered items and optional clickable source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily report output is capped at 15 total items, with all current 优设读报 items included first and remaining slots filled from 36氪 and 虎嗅.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
