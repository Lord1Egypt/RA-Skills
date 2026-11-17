## Description:

Digital Oracle helps agents answer macro, market, geopolitical, and asset-pricing probability questions by cross-validating trading-data signals from prediction markets, prices, derivatives, yield curves, filings, and related public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agent users use this skill to produce structured probability reports for questions that can be informed by real-money market pricing. It selects multiple independent trading-data signals, fetches them from provider APIs or web search, and explains how those prices support or contradict a forecast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to public market-data and web-search sources from the agent environment.

Mitigation: Run it in a sandbox or with egress controls and approve network access only for expected public data sources.

Risk: The web page fetcher can reach arbitrary URLs, including untrusted or user-supplied pages.

Mitigation: Avoid fetch_page for untrusted URLs in sensitive networks and review fetched sources before relying on their content.

Risk: Yahoo price and options providers depend on yfinance, which is outside the standard-library provider set.

Mitigation: Pin and review yfinance before enabling those providers.

## Reference(s):

- [Digital Oracle ClawHub Skill Page](https://clawhub.ai/komako-workshop/skills/digital-oracle)
- [Provider API Reference](references/providers.md)
- [Trading Symbols Directory](references/symbols.md)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown probability report with tables, scenario estimates, reasoning chains, and optional inline Python or shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv. Most providers use the Python standard library; Yahoo price and options providers require reviewing and installing yfinance.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
