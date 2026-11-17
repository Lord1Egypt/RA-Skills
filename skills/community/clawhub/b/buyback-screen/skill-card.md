## Description:

Screens A-share companies on the Shanghai, Shenzhen, and Beijing exchanges for recent buyback announcements and filters results by PE-TTM, PB, market cap, buyback amount, purpose, and progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-dreamer](https://clawhub.ai/user/lucky-dreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to screen recent A-share buyback plans, progress notices, and completed buybacks, then narrow the results by valuation, buyback size, purpose, progress, and date window. The output supports market-data review and report preparation, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Eastmoney public data endpoints during normal use.

Mitigation: Run it only in environments where outbound access to those public endpoints is acceptable.

Risk: The skill writes a TSV report file locally and allows a custom output path.

Mitigation: Review the --out path before execution, especially in shared directories.

Risk: The generated screen is market data and may be mistaken for investment advice.

Mitigation: Treat the output as a screening aid and verify any financial conclusions with appropriate sources and review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucky-dreamer/skills/buyback-screen)
- [ClawHub publisher profile](https://clawhub.ai/user/lucky-dreamer)
- [Eastmoney Data Center API endpoint](https://datacenter-web.eastmoney.com/api/data/v1/get)
- [Eastmoney stock announcement API endpoint](https://np-anotice-stock.eastmoney.com/api/security/ann?sr=-1&page_size=50&page_index=1&ann_type=A&client_source=web&stock_list=000333)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown table on stdout and UTF-8 TSV report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes announcement date, ticker, name, exchange, buyback amount, price cap, PE-TTM, PB, current price, market cap, purpose, progress, and profit/loss status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
