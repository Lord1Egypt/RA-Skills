## Description:

Fetch real-time crypto and market news from major sources for market news requests, token-specific updates, and market overviews before trading decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch recent crypto headlines, filter them by token or topic, and turn the results into concise market summaries. It is useful for situational awareness before trade-related discussions, but its sentiment labels should remain informational.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public crypto-news RSS feeds.

Mitigation: Review network access expectations before installation and restrict execution to environments where public RSS requests are acceptable.

Risk: Headlines and sentiment summaries may be incomplete, stale, or unsuitable as trading advice.

Mitigation: Treat generated summaries as informational only and verify source articles before making financial decisions.

Risk: Broad trigger language may activate the skill for general market-news requests.

Mitigation: Narrow trigger language when deployment should only handle explicit crypto-news requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuelhsin/skills/crypto-market-news)
- [CoinDesk RSS feed](https://feeds.feedburner.com/CoinDesk)
- [CoinTelegraph RSS feed](https://cointelegraph.com/rss)
- [Decrypt RSS feed](https://decrypt.co/feed)
- [CryptoSlate RSS feed](https://cryptoslate.com/feed/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with headlines, source links, and sentiment labels; shell output from RSS fetches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional keyword and lookback-hours arguments; no API key required.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
