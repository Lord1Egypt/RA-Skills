## Description: <br>
Generates a daily cryptocurrency report from news, market, DeFi yield, meme trend, funding, and policy sources, then formats it as three Telegram messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockpunk2077](https://clawhub.ai/user/blockpunk2077) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Crypto content operators and analysts use this skill to assemble a structured daily market report from live news, price, DeFi, meme, funding, and policy sources and publish it to a Telegram topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently publish reports to a fixed Telegram chat and topic. <br>
Mitigation: Verify the destination before use and require preview or confirmation before any report is sent. <br>
Risk: Broad trigger phrases can start publishing behavior when the user only intended to discuss a report. <br>
Mitigation: Narrow activation phrases to explicit publish commands and require confirmation for ambiguous requests. <br>
Risk: The skill reads a local API token and calls external crypto data services. <br>
Mitigation: Use an explicit scoped secret for the required APIs, limit token permissions, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blockpunk2077/crypto-daily-report) <br>
- [BlockBeats newsflash](https://www.theblockbeats.info/newsflash) <br>
- [Odaily newsflash](https://www.odaily.news/zh-CN/newsflash) <br>
- [CoinDesk latest crypto news](https://www.coindesk.com/latest-crypto-news) <br>
- [DeFiLlama yields](https://defillama.com/yields) <br>
- [GeckoTerminal Solana pools](https://www.geckoterminal.com/solana/pools) <br>
- [DEXScreener Solana fallback](https://dexscreener.com/solana) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls] <br>
**Output Format:** [Telegram Markdown split into three messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages are designed to stay under Telegram length limits and may be sent silently to a configured chat and topic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
