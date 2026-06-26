## Description: <br>
Coin research and crypto token analysis with CoinMarketCap (CMC) CLI for price, market cap, volume, on-chain stats, historical OHLCV, trading pairs, news sentiment, and bull or bear assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coinmarketcap-official](https://clawhub.ai/user/coinmarketcap-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external analysts use this skill to produce structured single-coin crypto research reports from CoinMarketCap CLI data. The workflow resolves a target asset, gathers market, fundamentals, liquidity, historical price, and news data, then synthesizes an informational bull, bear, and verdict assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires agent access to CMC_API_KEY and can make CoinMarketCap CLI requests for user-selected coins. <br>
Mitigation: Use a quota-limited API key where possible and only run the skill in sessions where CoinMarketCap API access is appropriate. <br>
Risk: The skill depends on an external cmc CLI binary. <br>
Mitigation: Verify the installed cmc CLI source before use and keep it updated through the trusted installation channel. <br>
Risk: Generated crypto research reports may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis only and review findings independently before making financial decisions. <br>


## Reference(s): <br>
- [CoinMarketCap CLI](https://github.com/openCMC/CoinMarketCap-CLI) <br>
- [ClawHub Skill Page](https://clawhub.ai/coinmarketcap-official/coin-crypto-research-cmc-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research report with inline shell commands and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cmc CLI and CMC_API_KEY; reports are informational and not financial advice.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
