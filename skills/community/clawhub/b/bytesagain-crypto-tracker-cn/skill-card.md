## Description:

Tracks cryptocurrency prices, market sentiment, DeFi TVL, trending and meme coins, technical indicators, yield comparisons, gas fees, portfolios, and price alerts using public crypto APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check crypto market data, compare DeFi metrics, calculate simple technical indicators, and manage local portfolio or alert records. Its educational strategy content should be treated as reference material, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes under-disclosed local finance tracking and financial-data storage behavior.

Mitigation: Review the included finance tracker before installation and only use it when local storage of holdings, alerts, transaction descriptions, and history is acceptable.

Risk: Portfolio, alert, and finance-history data may contain sensitive financial information on shared machines.

Mitigation: Use a private machine or tighten file permissions before entering portfolio details, alerts, or transaction descriptions.

Risk: The skill contacts public crypto APIs for market, DeFi, sentiment, yield, and gas data.

Mitigation: Run it only in environments where outbound requests to public crypto data services are permitted.

Risk: The skill includes educational strategy content and market signals that could be mistaken for investment advice.

Mitigation: Treat outputs as informational only and require independent review before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-crypto-tracker-cn)
- [BytesAgain homepage](https://bytesagain.com)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [DefiLlama API](https://api.llama.fi)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal-oriented text with inline shell commands and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact public crypto APIs and may write portfolio, alert, history, and finance-tracking data to local files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
