## Description:

Generates a structured Chinese daily cryptocurrency report from news, price, DeFi yield, meme trend, funding, and market data sources, then formats it for Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockpunk2077](https://clawhub.ai/user/blockpunk2077)

### License/Terms of Use:


## Use Case:

External users and crypto market operators use this skill to collect current cryptocurrency news and market signals and produce a daily Chinese report formatted for Telegram publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently posts generated reports to a hardcoded Telegram chat and thread.

Mitigation: Replace the destination with trusted local configuration and require explicit confirmation before any message is sent.

Risk: The workflow reads an OpenNews token from ~/.openclaw/.env.

Mitigation: Use a scoped secret mechanism and avoid direct reads from broad local environment files where possible.

Risk: The news fetch helper writes fetched pages to predictable /tmp filenames.

Mitigation: Use unique temporary files or a restricted temporary directory and clean up fetched content after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockpunk2077/skills/crypto-daily-report)
- [BlockBeats newsflash](https://www.theblockbeats.info/newsflash)
- [Odaily newsflash](https://www.odaily.news/zh-CN/newsflash)
- [PANews newsflash](https://www.panewslab.com/zh/newsflash)
- [CoinDesk latest crypto news](https://www.coindesk.com/latest-crypto-news)
- [DeFiLlama yields](https://defillama.com/yields)
- [GeckoTerminal Solana pools](https://www.geckoterminal.com/solana/pools/{pool_id})
- [DEXScreener Solana token fallback](https://dexscreener.com/solana/{addr})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Three Telegram-ready Markdown messages plus a final NO_REPLY marker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese report output is structured into headline, funding, updates, alpha, on-chain DeFi, viewpoint, trading data, and macro policy sections with per-message character limits.]

## Skill Version(s):

1.0.0 (source: _meta.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
