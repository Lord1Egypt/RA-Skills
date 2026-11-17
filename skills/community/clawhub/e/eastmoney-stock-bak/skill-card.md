## Description:

Helps agents answer stock-market questions with delayed quote summaries, price changes, trading volume, sector rankings, and watchlist-style stock lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask natural-language stock questions to obtain delayed quote summaries and sector rankings for A-share, Hong Kong, and U.S. equities. Treat outputs as informational market data, not as investment advice or a trading signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quotes, rankings, or recommendations may be delayed, inaccurate, or presented as current when static advisory content is mixed with fetched data.

Mitigation: Confirm any quote, ranking, or recommendation against a trusted financial source before acting on it.

Risk: Some market-data calls use plaintext HTTP.

Mitigation: Run the skill only in a controlled environment and prefer verified HTTPS data sources for any decision-making workflow.

Risk: The skill may misrepresent which financial data providers its outputs come from.

Mitigation: Disclose that outputs may come from mixed providers and do not present the skill as an authoritative Eastmoney-only source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/make453/skills/eastmoney-stock-bak)
- [Sina quote endpoint used by artifact](https://hq.sinajs.cn/list={code})
- [Eastmoney sector ranking endpoint used by artifact](http://push2.eastmoney.com/api/qt/clist/get)
- [Sina Finance](http://finance.sina.com.cn)
- [Eastmoney quote center](http://quote.eastmoney.com/center/gridlist.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with stock quote tables, sector rankings, command examples, and cautionary guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data may be delayed by several minutes, and some artifact outputs include static advisory commentary.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
