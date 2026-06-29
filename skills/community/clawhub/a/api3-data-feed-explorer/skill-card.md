## Description: <br>
Explore and analyze Api3 data feeds using public data, including provider coverage, aggregation composition, latest prices, on-chain versus off-chain staleness, provider deviations, and exchange spot-price comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metobom](https://clawhub.ai/user/metobom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect Api3 dAPI health, provider coverage, feed freshness, price deviations, and on-chain versus off-chain gaps using public data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public Api3, blockchain RPC, and exchange endpoints. <br>
Mitigation: Run it in an environment where network access to expected public endpoints is acceptable and review endpoint access before deployment. <br>
Risk: Results depend on live third-party data that can be stale, unavailable, or divergent across sources. <br>
Mitigation: Run scripts fresh for each question, report timestamps and data age, and treat exchange comparisons as advisory checks rather than a source of truth. <br>
Risk: Dependency behavior can change at install time because the package manifest uses a latest-version dependency. <br>
Mitigation: Pin and review dependency versions before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/metobom/api3-data-feed-explorer) <br>
- [Api3 Signed API public endpoint example](https://signed-api.api3.org/public/0xBA910Eb2867977A0a651FE3D2607237ff4116B1C) <br>
- [Binance ticker price API](https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT) <br>
- [Coinbase spot price API](https://api.coinbase.com/v2/prices/BTC-USD/spot) <br>
- [Kraken public ticker API](https://api.kraken.com/0/public/Ticker?pair=XBTUSD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and tabular analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports depend on fresh public Api3, blockchain RPC, and exchange responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and SKILL.md frontmatter; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
