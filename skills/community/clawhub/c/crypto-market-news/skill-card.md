## Description: <br>
Fetches recent cryptocurrency market news from public RSS feeds and helps agents summarize headline sentiment and market-relevance signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for recent crypto market news, token-specific headlines, or a broad market overview before making their own trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public news feeds. <br>
Mitigation: Run it only in environments where network access to the configured RSS sources is acceptable. <br>
Risk: The hours argument has a minor input-validation caveat. <br>
Mitigation: Provide simple numeric lookback values such as 24 or 48 hours. <br>
Risk: Headline sentiment and trading-impact notes can be mistaken for financial advice. <br>
Mitigation: Treat the output as news context only and verify important claims before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub listing: Crypto Market News](https://clawhub.ai/samuelhsin/crypto-market-news) <br>
- [CoinDesk RSS feed](https://feeds.feedburner.com/CoinDesk) <br>
- [CoinTelegraph RSS feed](https://cointelegraph.com/rss) <br>
- [Decrypt RSS feed](https://decrypt.co/feed) <br>
- [CryptoSlate RSS feed](https://cryptoslate.com/feed/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with shell command snippets, headline summaries, links, and sentiment notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to five recent matching articles per configured RSS source; requires curl and python3 at execution time.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
