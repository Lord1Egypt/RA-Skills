## Description: <br>
每日新闻自动采集与报告生成，使用双引擎交叉验证、官方媒体优先和 900 秒超时容错生成中文日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-language users and agent operators use this skill to generate a dated daily public-news report covering politics, finance, AI, technology, consumer electronics, and home appliances. It returns the full Markdown report and saves a dated local copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs multiple web searches and may collect or summarize public news that later changes or proves inaccurate. <br>
Mitigation: Review cited sources and credibility markers before relying on the report for decisions. <br>
Risk: The skill saves dated report copies locally under memory/, which may retain news content longer than intended. <br>
Mitigation: Disable, rotate, or delete the local archive when retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/daily-news-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Markdown report with categorized numbered news items, source labels, and credibility markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Also saves a dated copy under memory/daily_news_YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
