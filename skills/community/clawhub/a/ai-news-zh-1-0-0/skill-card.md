## Description:

Ai News Zh collects English-language AI news, translates and organizes it into a Chinese daily briefing, and can deliver it to Feishu, Telegram, or Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pppig1357](https://clawhub.ai/user/pppig1357)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language users who follow the AI industry use this skill to collect, deduplicate, translate, categorize, and receive daily AI news briefings from public English-language sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled delivery can send briefings to an unintended Feishu, Telegram, or Discord destination if the channel is configured incorrectly.

Mitigation: Set the exact destination before enabling scheduled delivery or the message tool, then perform a manual run to confirm the content and channel.

Risk: Briefings are generated from public news sources and automated translation, so individual items may contain source inaccuracies, stale information, or translation errors.

Mitigation: Review important items against the included source URLs before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pppig1357/skills/ai-news-zh-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/pppig1357)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss)
- [TechCrunch RSS](https://techcrunch.com/feed/)
- [Anthropic News](https://www.anthropic.com/news)
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/)
- [Google AI Blog](https://blog.google/technology/ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown daily briefing with Chinese headlines, summaries, source links, category labels, and a short trend observation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 8-12 news items per briefing; messaging delivery depends on configured Feishu, Telegram, or Discord destination.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
