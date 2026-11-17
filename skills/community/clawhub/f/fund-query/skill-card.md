## Description:

查询场外基金（公募基金）的实时估值、净值、基本信息。支持天天基金代码查询。当用户询问基金净值、基金估值、基金涨跌时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up public mutual fund estimates, net asset values, basic fund information, and recent historical values by six-digit fund code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund data is fetched over unauthenticated HTTP and could be intercepted or modified on the network.

Mitigation: Treat returned values as informational and verify important financial data through trusted sources before making decisions.

Risk: The skill contacts public fund-data APIs for each fund code the user asks about.

Mitigation: Use only fund codes you are comfortable sending to those public services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pazzilivo/skills/fund-query)
- [Publisher profile](https://clawhub.ai/user/pazzilivo)
- [天天基金网 public API](http://fund.eastmoney.com/)
- [Fund estimate endpoint](http://fundgz.1234567.com.cn/js/{fund_code}.js)
- [Fund detail endpoint](http://fund.eastmoney.com/pingzhongdata/{fund_code}.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like text with formatted fund lookup results and JSON error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a six-digit fund code and optionally an estimate, info, or history command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
