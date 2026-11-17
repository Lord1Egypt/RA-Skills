## Description:

FTShare Market Data routes agent requests to FT market-data services for A-share, Hong Kong, and US stock data, ETFs, funds, indexes, macroeconomic indicators, market news, valuations, K-lines, index weights, and related financial datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize market data for A-share, Hong Kong, and US securities, including quotes, K-lines, fundamentals, fund and ETF data, index data, macro indicators, financial calendars, and related news. It is intended for data lookup and analysis support, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes HTTPS requests to external FT market-data services.

Mitigation: Use it only where outbound access to those services is acceptable, and treat returned market data as provider-supplied information that may need independent verification.

Risk: Download routes can write PDF, XML, or XLSX files into the current working directory.

Mitigation: Use explicit output filenames in an appropriate working directory and review downloaded files before opening, sharing, or relying on them.

Risk: Some documented announcement or report routes may be stale or unavailable.

Mitigation: Handle route failures gracefully and confirm availability before building workflows that depend on those routes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawn92/skills/ftshare-market-data)
- [FT Market Data API Documentation](https://market.ft.tech/gateway/doc)
- [FT Market Data Service](https://market.ft.tech)
- [FT AI Chat Service](https://ftai.chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [JSON data that agents can summarize as Markdown tables or bullets; selected download routes may write PDF, XML, or XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data is returned from external HTTPS services and should be treated as provider-supplied financial data.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
