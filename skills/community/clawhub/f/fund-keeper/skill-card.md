## Description:

Chinese mutual fund intelligent advisor with real-time valuation, buy/sell suggestions, profit tracking, SIP planning, OCR recognition, and stock-fund linkage. Supports offline mode and multi-source caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangepier-crypto](https://clawhub.ai/user/tangepier-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Fund Keeper to track Chinese mutual fund portfolios, review valuation and profit reports, manage SIP plans and alerts, and generate reference buy/sell guidance from public market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial guidance and market-data integrity

Mitigation: Treat investment suggestions and sample stock rankings as unverified reference output; review data freshness and do not use the skill as the sole basis for investment decisions.

Risk: Network access to public market-data services

Mitigation: Run the skill in a dedicated environment with restricted network access to the declared market-data domains where possible.

Risk: Local portfolio persistence and bundled records

Mitigation: Remove bundled portfolio data before use and avoid storing sensitive financial records in shared workspaces.

Risk: Recurring scheduled tasks

Mitigation: Enable scheduled checks only after reviewing the commands, permissions, and output locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tangepier-crypto/skills/fund-keeper)
- [TTJJ fund valuation endpoint](http://fundgz.1234567.com.cn/js/{fund_code}.js)
- [EastMoney fund page](https://fund.eastmoney.com/{code}.html)
- [Sina Finance quotes](http://hq.sinajs.cn/list=fu_{fund_code})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and Markdown with shell command examples and JSON-backed local configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, transaction, cache, statistics, and SIP-plan files under the funds directory.]

## Skill Version(s):

2.6.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
