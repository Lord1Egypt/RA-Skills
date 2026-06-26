## Description: <br>
每日新闻自动采集与报告生成。使用 web_search (freshness=oneDay) 替代旧版 Bing/Tavily 方案，确保新闻均为24小时内真实最新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manually or routinely collect recent public news and produce a concise daily Chinese Markdown report across politics, finance, AI, technology, and consumer electronics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled weekday runs and local report archives can retain old daily news reports longer than intended. <br>
Mitigation: Review the weekday cron behavior before enabling scheduled use, and periodically delete memory/daily_news_*.md when retained reports are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown daily news report saved as memory/daily_news_{YYYY-MM-DD}.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one-day freshness searches across seven news categories, filters old or noisy results, and keeps a local report archive.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
