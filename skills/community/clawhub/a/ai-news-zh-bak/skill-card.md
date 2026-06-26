## Description: <br>
中文AI科技日报自动采集与推送。从The Verge、Wired、TechCrunch等英文源抓取最新AI资讯，自动翻译整理为中文，按分类推送到飞书/Telegram/Discord等渠道。适合关注AI行业动态的中文用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitsarp](https://clawhub.ai/user/gitsarp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking AI news readers and operators use this skill to fetch English-language AI news, translate and classify it, and prepare a concise Chinese daily briefing for manual review or configured channel posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public AI news sources and may collect incomplete, stale, duplicated, or incorrectly classified stories. <br>
Mitigation: Run the skill manually first and review the generated briefing, including source links, before relying on scheduled output. <br>
Risk: If channel posting is configured, a briefing could be sent to an unintended or overly broad audience. <br>
Mitigation: Use a limited test destination before enabling scheduled posting to Feishu, Telegram, Discord, or another channel. <br>
Risk: Optional web search may require an API key. <br>
Mitigation: Keep any optional search API key scoped to search-only access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitsarp/ai-news-zh-bak) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss) <br>
- [TechCrunch RSS](https://techcrunch.com/feed/) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/) <br>
- [Google AI Blog](https://blog.google/technology/ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown daily briefing in Chinese with categorized items, source links, and a short trend insight] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically 8-12 news items, ordered by importance and deduplicated across runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
