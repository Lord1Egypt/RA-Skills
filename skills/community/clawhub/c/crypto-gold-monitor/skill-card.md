## Description: <br>
加密货币与贵金属价格监控 / Crypto & Precious Metals Price Monitor - 监控BTC/ETH实时价格、黄金(XAU)/白银(XAG)走势，免费API无需Key <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franky0617](https://clawhub.ai/user/franky0617) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and individual users use this skill to monitor BTC, ETH, gold, silver, and USD/CNY prices from a local shell workflow. It is suited for quick market visibility and threshold-style awareness, not for investment advice or guaranteed real-time pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party market-data APIs when run. <br>
Mitigation: Review the listed data-source endpoints against local network policy before deployment. <br>
Risk: The skill writes temporary price cache files under /tmp/crypto-monitor. <br>
Mitigation: Run in an environment where temporary cache files are acceptable and clear the cache when stale or unwanted. <br>
Risk: Displayed prices may be delayed, estimated, rate-limited, or unavailable and should not be treated as investment advice. <br>
Mitigation: Verify prices against authoritative financial data sources before making trading or investment decisions. <br>
Risk: The local command may require setup and common shell dependencies such as curl, python3, and bc. <br>
Mitigation: Confirm dependencies and command installation before relying on the monitor in routine workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/franky0617/crypto-gold-monitor) <br>
- [CoinGecko simple price API endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24h_change=true) <br>
- [ExchangeRate API USD endpoint](https://api.exchangerate-api.com/v4/latest/USD) <br>
- [GoldAPI XAU/USD endpoint](https://www.goldapi.io/api/XAU/USD) <br>
- [Yahoo Finance XAU/USD chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X?interval=1m&range=1d) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text output with shell command examples and local JSON cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market-data APIs when run and stores temporary cache files under /tmp/crypto-monitor.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
