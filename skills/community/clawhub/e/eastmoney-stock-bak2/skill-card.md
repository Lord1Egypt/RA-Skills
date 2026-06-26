## Description: <br>
Queries Eastmoney-style stock data, including individual quotes, percentage changes, trading volume, and stock-market rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market watchers use this skill to ask an agent for public stock quotes, gain/loss rankings, volume, turnover, and watchlist-style summaries for A-shares, Hong Kong stocks, and U.S. stocks. It should be used as an informational market-data helper, not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock picks, stop-losses, and portfolio-allocation examples could be mistaken for current market data or investment advice. <br>
Mitigation: Use only as a public market-data helper; verify quotes and rankings with a trusted source and do not rely on stock picks, stop-losses, or allocations as investment advice. <br>
Risk: Public quote and ranking data may be delayed, unavailable, or inconsistent across providers. <br>
Mitigation: Check timestamps and confirm material decisions against a trusted market-data or trading platform before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/make453/eastmoney-stock-bak2) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={code}) <br>
- [Eastmoney sector ranking endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown market summaries with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include delayed public market data, rankings, brief analysis, and cautionary notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
