## Description: <br>
中文AI科技日报自动采集与推送，从 The Verge、Wired、TechCrunch 等英文源抓取最新 AI 资讯，自动翻译整理为中文，并按分类推送到飞书、Telegram、Discord 等渠道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aizain](https://clawhub.ai/user/aizain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Chinese-speaking AI readers and operators use this skill to collect recent AI news from English-language sources, translate and categorize the stories, and publish a concise Chinese daily briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled posting can send unwanted or incorrect briefings to configured messaging channels. <br>
Mitigation: Run a manual preview before scheduling, confirm the target channel, and keep the cron job or channel configuration easy to disable. <br>
Risk: Optional search or messaging credentials can grant broader access than the digest workflow needs. <br>
Mitigation: Use least-privilege credentials for search and messaging integrations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aizain/ai-news-zh) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss) <br>
- [TechCrunch RSS](https://techcrunch.com/feed/) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/) <br>
- [Google AI Blog](https://blog.google/technology/ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown daily briefing in Chinese with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 8-12 deduplicated news items ordered by importance, with category tags and a closing trend observation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
