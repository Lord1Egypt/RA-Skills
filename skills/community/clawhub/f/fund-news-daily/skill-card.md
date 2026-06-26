## Description: <br>
Collects public fund news from five Chinese financial news sources, filters excluded private-fund, interview, market-commentary, ETF leaderboard, and fund-flow items, and returns structured summaries with optional Word reports for weekly or date-range queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yujing2013](https://clawhub.ai/user/Yujing2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect public fund-industry news from specified Chinese financial news sites, apply the included filtering rules, and produce structured daily, weekly, or date-range reports. Longer-range queries can also create a local Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install npm and pip dependencies, including a global agent-browser package. <br>
Mitigation: Use an isolated environment or preinstall reviewed versions of agent-browser and python-docx before running the skill. <br>
Risk: The skill fetches public news pages and summarizes or extracts article content for reports. <br>
Mitigation: Review generated summaries and source links before using the report for business or investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Yujing2013/fund-news-daily) <br>
- [Publisher profile](https://clawhub.ai/user/Yujing2013) <br>
- [内容筛选规则](artifact/references/filter_rules.md) <br>
- [时间查询规则](artifact/references/query_rules.md) <br>
- [技术实现细节](artifact/references/technical_specs.md) <br>
- [Word文档格式规范](artifact/references/word_format.md) <br>
- [证券时报基金新闻](http://www.stcn.com/article/list/fund.html) <br>
- [中国证券报基金动态](https://www.cs.com.cn/tzjj/jjdt/) <br>
- [证券日报基金](http://www.zqrb.cn/fund/) <br>
- [上海证券报基金](https://www.cnstock.com/channel/10033) <br>
- [中国基金报基金](https://www.chnfund.com/fund) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Structured Chinese text or Markdown, with optional .docx Word document output for weekly and date-range reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [First use may install agent-browser globally with npm and python-docx with pip; report content includes source, time, title, summary, and official link fields.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
