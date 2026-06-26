## Description: <br>
Provides fund net asset value lookup, historical trend analysis, fund screening and ranking, holdings analysis, and fund comparison using public fund-data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hl950825](https://clawhub.ai/user/hl950825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve public fund data, compare fund performance, screen ranked funds, and summarize fund holdings for informational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund codes and screening choices are sent to public fund-data websites. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering private account details, cookies, or logged-in session data. <br>
Risk: Fund data may be delayed, incomplete, or affected by source-site changes. <br>
Mitigation: Treat results as informational and verify investment decisions against official or primary financial sources. <br>
Risk: Artifact documentation describes different primary data sources in different places. <br>
Mitigation: Review outputs with awareness that scripts primarily call Tiantian Fund or Eastmoney endpoints, while some documentation mentions Alipay fund pages. <br>


## Reference(s): <br>
- [Fund Analyzer usage guide](artifact/references/guide.md) <br>
- [ClawHub fund-analyzer release page](https://clawhub.ai/hl950825/fund-analyzer) <br>
- [Tiantian Fund ranking data](https://fund.eastmoney.com/data/fundranking.html) <br>
- [Tiantian Fund detail page pattern](https://fund.eastmoney.com/${fund_code}.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tabular or list-style fund analysis and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current fund values, historical return summaries, ranking lists, holdings summaries, and data-source reliability notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
