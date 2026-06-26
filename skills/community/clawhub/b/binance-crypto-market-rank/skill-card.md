## Description: <br>
Provides crypto market rankings and leaderboards for trending tokens, Binance Alpha tokens, smart money inflows, meme tokens, and top trader PnL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexploarer](https://clawhub.ai/user/dexploarer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and agents use this skill to fetch and summarize public Binance Web3 ranking data for token discovery, market trend review, smart-money inflow checks, meme token ranking, and trader leaderboard analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market rankings may be mistaken for financial advice or stable investment recommendations. <br>
Mitigation: Present results as live market data, cite the ranking type and timeframe, and avoid investment recommendations unless separately requested and verified. <br>
Risk: The skill runs a local shell script that contacts public Binance Web3 APIs. <br>
Mitigation: Review the script and network endpoints before deployment, use only public data, and do not provide credentials. <br>
Risk: Publisher provenance is unavailable for this release. <br>
Mitigation: Verify the dexploarer publisher profile and any claimed Binance affiliation before treating the release as official. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dexploarer/binance-crypto-market-rank) <br>
- [Publisher profile](https://clawhub.ai/user/dexploarer) <br>
- [Binance Web3 unified token rank endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list/ai) <br>
- [Binance Web3 smart money inflow endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/tracker/wallet/token/inflow/rank/query/ai) <br>
- [Binance Web3 meme rank endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/exclusive/rank/list/ai) <br>
- [Binance Web3 trader leaderboard endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/market/leaderboard/query/ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [JSON from a shell script plus an agent-authored Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches live public market data from Binance Web3 endpoints; values may change over time and should not be treated as financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version is 2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
