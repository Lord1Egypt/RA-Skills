## Description: <br>
Daily coin market report and crypto snapshot via the CoinMarketCap CLI, covering BTC and ETH prices, top gainers and losers, trending tokens, and latest crypto news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coinmarketcap-official](https://clawhub.ai/user/coinmarketcap-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate concise crypto market snapshots and daily market reports from CoinMarketCap CLI data. It is suited for market report, crypto morning brief, crypto market summary, and similar workflow requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external cmc CLI and CoinMarketCap API key. <br>
Mitigation: Verify the cmc CLI comes from the intended CoinMarketCap CLI project and provide CMC_API_KEY through secure skill configuration or session environment. <br>
Risk: Generated crypto market reports may be mistaken for financial advice. <br>
Mitigation: Treat reports as market information, include risks and caveats, and avoid presenting generated summaries as investment recommendations. <br>
Risk: Market data, news, or command output may be incomplete, stale, or unavailable. <br>
Mitigation: Return partial sections with clear notes about missing or stale data and continue the report using available command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coinmarketcap-official/crypto-market-report-cmc-cli) <br>
- [CoinMarketCap CLI](https://github.com/openCMC/CoinMarketCap-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with ordered market sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cmc CLI and CMC_API_KEY; reports include market snapshot, BTC and ETH, momentum, news flow, and risks or caveats.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
