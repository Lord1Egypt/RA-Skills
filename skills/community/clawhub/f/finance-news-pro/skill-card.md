## Description: <br>
财经新闻深度分析技能。从多个财经源抓取内容，进行情感分析（利好/利空/中性）、影响评估（行业/公司/市场）、关键信息提取，生成专业投资简报。支持 A 股/港股/美股、行业板块、个股分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and finance-focused agent users use this skill to gather financial news from multiple public sources and produce Chinese-language investment briefings with sentiment, impact level, stock association, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-activate on broad finance or news keywords and may browse public financial websites. <br>
Mitigation: Use explicit invocations, review configured sources and cron/watch settings, and confirm that browsing is expected before enabling automated runs. <br>
Risk: Generated reports can include investment-oriented labels, market sentiment, and operation advice that may be incomplete or misleading. <br>
Mitigation: Treat outputs as research summaries rather than financial advice, verify material claims against original sources, and include source links and timestamps in reports. <br>
Risk: The skill may save local reports and cached news data. <br>
Mitigation: Choose an appropriate output directory, avoid entering sensitive portfolio details unless needed, and review stored files before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SuCriss/finance-news-pro) <br>
- [Publisher profile](https://clawhub.ai/user/SuCriss) <br>
- [财联社电报](https://www.cls.cn/telegraph) <br>
- [华尔街见闻快讯](https://www.wallstreetcn.com/live) <br>
- [东方财富快讯](https://news.eastmoney.com/kx/) <br>
- [雪球热点](https://xueqiu.com/hots) <br>
- [财新](https://www.caixin.com/) <br>
- [第一财经](https://www.yicai.com/) <br>
- [界面新闻](https://www.jiemian.com/) <br>
- [央行官网](http://www.pbc.gov.cn/) <br>
- [证监会](http://www.csrc.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Chinese Markdown investment briefing plus structured JSON output and optional local report/cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include source links, timestamps, sentiment labels, impact levels, related stock mappings, operation advice, and market filters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
