## Description:

Queries stock data for Eastmoney-style stock questions, including individual quotes, price changes, volume, and market ranking information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongchun2008](https://clawhub.ai/user/dongchun2008)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Chinese-language stock questions by fetching individual quotes, sector gain/loss rankings, and watchlist-style stock information. It is suited for informational market lookup, not financial advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill is under-disclosed because individual stock quote queries are sent to Sina Finance despite Eastmoney branding.

Mitigation: Disclose the Sina Finance quote source to users and verify returned quote data against a trusted market-data source before relying on it.

Risk: The security scan reports that sector data is fetched from an unencrypted Eastmoney HTTP endpoint.

Mitigation: Run the skill in a trusted environment, avoid submitting sensitive watchlists where network observers are a concern, and switch to HTTPS if the provider supports it.

Risk: The security guidance notes that advertised Hong Kong and U.S. stock support may not work reliably and that market data may be delayed.

Mitigation: Treat results as informational, test supported markets before release, and confirm time-sensitive prices with an authoritative source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongchun2008/skills/eastmoney-stock)
- [Publisher profile](https://clawhub.ai/user/dongchun2008)
- [Eastmoney sector ranking API endpoint](http://push2.eastmoney.com/api/qt/clist/get)
- [Eastmoney quote center](http://quote.eastmoney.com/center/gridlist.html)
- [Sina Finance quote API endpoint](https://hq.sinajs.cn/list={code})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown-formatted stock quote and sector ranking reports, with command-line text output from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data depends on external finance endpoints and may be delayed by a few minutes.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
