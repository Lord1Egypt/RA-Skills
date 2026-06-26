## Description: <br>
Queries stock data described as Eastmoney data, including individual quotes, price changes, volume, and rankings for stock-related questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to retrieve stock quote summaries, market-sector rankings, and stock-related analysis for A-share, Hong Kong, and U.S. market queries. Outputs should be treated as informational research, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present delayed, mixed-source, or hard-coded stock data as live market information. <br>
Mitigation: Verify all quotes, rankings, timestamps, and source labels against a trusted live market-data provider before acting on them. <br>
Risk: Some artifact behavior includes stock picks, allocation suggestions, and stop-loss guidance. <br>
Mitigation: Treat recommendations as non-authoritative research only and do not use them as financial, trading, or portfolio advice. <br>
Risk: The skill calls third-party finance endpoints and depends on their availability and response formats. <br>
Mitigation: Review the scripts before installation and handle API failures, stale data, and parsing errors in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/make453/eastmoney-stock-bak) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={code}) <br>
- [Eastmoney sector ranking endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>
- [Eastmoney market quote page](http://quote.eastmoney.com/center/gridlist.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown-like text summaries with quote tables, rankings, and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include delayed market data, third-party API results, hard-coded examples, and stock-related guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
