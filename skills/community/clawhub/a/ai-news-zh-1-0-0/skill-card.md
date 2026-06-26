## Description: <br>
中文AI科技日报自动采集与推送。从The Verge、Wired、TechCrunch等英文源抓取最新AI资讯，自动翻译整理为中文，按分类推送到飞书/Telegram/Discord等渠道。适合关注AI行业动态的中文用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pppig1357](https://clawhub.ai/user/pppig1357) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking AI practitioners, operators, and readers use this skill to collect English-language AI news, translate and classify it, and produce a concise daily Chinese briefing for manual review or channel posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may be posted to third-party messaging services when integrations are configured. <br>
Mitigation: Run the skill manually once, confirm the exact posting channel, and grant only limited bot or API permissions. <br>
Risk: Generated translations and summaries can omit context or misstate details from source articles. <br>
Mitigation: Review the selected stories and source links before relying on the briefing or distributing it broadly. <br>
Risk: Optional search or messaging integrations may require sensitive credentials. <br>
Mitigation: Store credentials in the agent environment or approved secret manager and avoid granting permissions beyond news collection and intended channel posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pppig1357/ai-news-zh-1-0-0) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss) <br>
- [TechCrunch RSS](https://techcrunch.com/feed/) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/) <br>
- [Google AI Blog](https://blog.google/technology/ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily briefing in Chinese with source links and category labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically 8-12 selected news items, ordered by importance, with a short trend insight.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
