## Description:

财经新闻深度分析技能：从多个财经源抓取内容，进行情感分析、影响评估、关键信息提取，并生成专业投资简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sucriss](https://clawhub.ai/user/sucriss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather Chinese-language financial news across A-share, Hong Kong, and U.S. market topics, classify sentiment and impact, link mentioned stocks, and draft Markdown briefings for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate on broad finance, stock, market, investment, company, or industry language.

Mitigation: Keep activation explicit and limit use to finance-news requests where the user clearly wants a briefing.

Risk: Generated sentiment labels and operation guidance may look like investment advice.

Mitigation: Treat outputs as non-personalized market information, preserve source links, and require human review before any trading or portfolio decision.

Risk: The fetch script can persist reports and cache files locally.

Mitigation: Use --no-save when local persistence is not desired, or review and clear the configured output directory.

Risk: Cron or watch-style usage can create recurring runs and repeated finance briefings.

Mitigation: Avoid scheduled or watch-mode execution unless a user intentionally configures it.

Risk: Optional HTTP, HTML parsing, RSS, and data-processing dependencies expand the local execution environment.

Mitigation: Install optional dependencies only in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sucriss/skills/finance-news-pro)
- [财联社电报](https://www.cls.cn/telegraph)
- [华尔街见闻 Live](https://www.wallstreetcn.com/live)
- [东方财富快讯](https://news.eastmoney.com/kx/)
- [雪球热门](https://xueqiu.com/hots)
- [中国人民银行](http://www.pbc.gov.cn/)
- [中国证券监督管理委员会](http://www.csrc.gov.cn/)
- [Seeking Alpha](https://seekingalpha.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown financial briefings with JSON-formatted processed news when the fetch script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save local Markdown reports and JSON cache files unless run with --no-save.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
