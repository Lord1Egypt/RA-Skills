## Description:

加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor - 监控BTC/ETH实时价格、黄金(XAU)/白银(XAG)走势，免费API无需Key

This skill is ready for commercial/non-commercial use.

## Publisher:

[franky0617](https://clawhub.ai/user/franky0617)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run a shell-based monitor for Bitcoin, Ethereum, gold, silver, and USD/CNY exchange-rate snapshots. It supports terminal display, refresh, and manual precious-metals update workflows for market reference, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script contacts third-party market APIs and consumes external API responses.

Mitigation: Review API dependencies before installation and validate API-derived values as numeric before regular use.

Risk: The shell script writes cache and history files under a shared temporary directory.

Mitigation: Move storage to a private per-user cache directory and avoid following symlinks.

Risk: Evidence notes advertised silver and 24-hour-change behavior may need correction.

Mitigation: Verify silver pricing and 24-hour change behavior against trusted data before relying on displayed market values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franky0617/skills/crypto-gold-monitor)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24h_change=true)
- [ExchangeRate API USD latest endpoint](https://api.exchangerate-api.com/v4/latest/USD)
- [GoldAPI XAU/USD endpoint](https://www.goldapi.io/api/XAU/USD)
- [Yahoo Finance XAU/USD chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X?interval=1m&range=1d)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays market prices and cached API-derived values; writes local cache and history JSON files during execution.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
