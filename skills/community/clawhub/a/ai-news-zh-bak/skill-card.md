## Description:

中文AI科技日报自动采集与推送。从The Verge、Wired、TechCrunch等英文源抓取最新AI资讯，自动翻译整理为中文，按分类推送到飞书/Telegram/Discord等渠道。适合关注AI行业动态的中文用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitsarp](https://clawhub.ai/user/gitsarp)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language AI readers and teams use this skill to collect recent English AI news, translate and categorize it into a concise daily briefing, and optionally deliver it to Feishu, Telegram, or Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled delivery may post a generated briefing to the wrong Feishu, Telegram, or Discord destination.

Mitigation: Run the skill manually once, verify the generated content, and confirm the exact destination before enabling scheduled delivery.

Risk: Translated news summaries may lose nuance or include source-content errors.

Mitigation: Review the briefing and source links before forwarding it to a broad audience.

## Reference(s):

- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss)
- [TechCrunch RSS](https://techcrunch.com/feed/)
- [Anthropic News](https://www.anthropic.com/news)
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/)
- [Google AI Blog](https://blog.google/technology/ai/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown daily briefing with Chinese headlines, summaries, source links, category labels, and a closing insight]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 8-12 deduplicated news items ordered by importance when enough current source material is available.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
