## Description:

获取 A 股市场日报，包括大盘指数、热门板块和龙头股。使用东方财富 API，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to generate a concise A-share market daily report covering major indices, top concept sectors, leading stocks, and a brief market comment. The output is informational and should not be used as the sole basis for trading or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data is fetched over plaintext HTTP.

Mitigation: Use the skill only where plaintext market-data requests are acceptable, and prefer updating endpoints to HTTPS if supported before relying on the output for analysis.

Risk: The Python dependency is not pinned.

Mitigation: Install dependencies in an isolated environment and pin or review the requests package version before operational use.

Risk: Financial output may be stale, incomplete, or unsuitable for investment decisions.

Mitigation: Treat the report as informational, verify important figures from a trusted market-data source, and do not use it as the sole basis for trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/a-stock-daily-report-cn)
- [Eastmoney quote API base endpoint](http://push2.eastmoney.com/api/qt)
- [Eastmoney stock quote endpoint](http://push2.eastmoney.com/api/qt/stock/get)
- [Eastmoney list quote endpoint](http://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text or Markdown market report with optional Python usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market figures are fetched from Eastmoney public endpoints at runtime; non-trading periods may show the latest closing data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
