## Description:

Provides BitoPro-scoped crypto market intelligence, listing-catalog lookup, and relevant news aggregation using public market and news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitopro](https://clawhub.ai/user/bitopro)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect market sentiment, BitoPro-listed coin rankings, public BTC/ETH treasury data, live BitoPro pair specifications, and BitoPro-relevant crypto news. It is informational only and does not place trades or access accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data, listings, mappings, and news can be stale, incomplete, rate limited, or unavailable.

Mitigation: Use live BitoPro pair lookup for current listings, degrade gracefully on API failures, show only sources actually queried, and ask users to verify investment decisions independently.

Risk: English RSS article titles and descriptions may be sent to Google Translate and machine translation can be inaccurate.

Mitigation: Translate only displayed English news items, disclose machine translation, and retain original-source links for verification.

Risk: Users may mistake informational market or news summaries for trading advice.

Mitigation: Keep responses factual, include investment-risk disclaimers for market data and news, and avoid buy, sell, or prediction language.

Risk: Users may try to use the skill for order placement, account access, or pre-trade workflows.

Mitigation: Keep this skill scoped to public information and direct trading or account actions to a separate trading-capable skill.

## Reference(s):

- [Endpoint reference](references/endpoints.md)
- [BitoPro coin mapping](references/coin-mapping.md)
- [News category keywords](references/news-categories.md)
- [CoinGecko Demo API dashboard](https://www.coingecko.com/en/developers/dashboard)
- [BitoPro skill page](https://clawhub.ai/bitopro/skills/bitopro-skill-hub)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite only sources actually queried and include investment-risk disclaimers for market data or news.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
