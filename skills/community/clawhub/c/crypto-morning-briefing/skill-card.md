## Description: <br>
Generate structured crypto market morning briefing via public web search, including market overview, key asset trends, macro and regulatory news, risk warnings, and information sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a concise crypto market morning briefing from public market data and recent crypto news. The briefing is informational and is not professional investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and depends on curl and jq, and execution may fail or require system package installation when those binaries are unavailable. <br>
Mitigation: Install the declared dependencies through the documented package command before use, and review package installation in environments with restricted system changes. <br>
Risk: The skill makes outbound requests to public crypto market and news services. <br>
Mitigation: Run it only in environments where outbound access to public crypto data and news services is acceptable. <br>
Risk: Crypto market output may be delayed, incomplete, or unsuitable for financial decision-making. <br>
Mitigation: Treat the briefing as informational only, verify important data against primary sources, and do not use it as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/crypto-morning-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [CoinGecko global market API](https://api.coingecko.com/api/v3/global) <br>
- [CoinGecko markets API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,binancecoin&order=market_cap_desc&per_page=4&page=1&sparkline=false) <br>
- [CryptoPanic public news RSS](https://cryptopanic.com/news/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown briefing by default, or JSON when invoked with --json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market overview, major asset updates, macro and regulatory news, risk warnings, and source names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
