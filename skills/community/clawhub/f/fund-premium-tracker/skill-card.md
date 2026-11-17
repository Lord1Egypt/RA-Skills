## Description:

Queries and analyzes real-time and historical premium or discount rates for A-share listed funds, including ETFs, LOFs, and QDII funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cantoneyes](https://clawhub.ai/user/cantoneyes)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent users use this skill to check whether a listed fund is trading above or below its NAV and to review recent premium trends before further research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some public finance data is fetched over plaintext HTTP, so market price or NAV data could be modified on an untrusted network.

Mitigation: Treat outputs as informational and verify important results with a trusted broker or official market source before making financial decisions.

Risk: QDII and cross-border fund NAV values may lag by one to two trading days, which can distort real-time premium calculations.

Mitigation: Check the displayed NAV date and use the result as a screening signal rather than a trading decision by itself.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cantoneyes/skills/fund-premium-tracker)
- [Publisher profile](https://clawhub.ai/user/cantoneyes)
- [Eastmoney market and fund data APIs](https://push2.eastmoney.com)
- [Eastmoney fund NAV data](http://api.fund.eastmoney.com)
- [Intraday fund estimate data](http://fundgz.1234567.com.cn)
- [Sina Finance fallback data](http://finance.sina.com.cn)
- [Tencent Finance fallback data](http://qt.gtimg.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal text with tables, percentages, source labels, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fund codes, market prices, NAV or intraday estimates, premium percentages, trend summaries, and risk prompts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
