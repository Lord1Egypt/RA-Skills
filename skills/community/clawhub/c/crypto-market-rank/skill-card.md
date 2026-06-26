## Description: <br>
Crypto market rankings and leaderboards for querying trending tokens, top searched tokens, Binance Alpha tokens, tokenized stocks, social hype sentiment ranks, smart money inflow token rankings, top meme token rankings from Pulse launchpad, and top trader PnL leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Awessh](https://clawhub.ai/user/Awessh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query public crypto market rankings, social sentiment leaderboards, smart money inflow rankings, meme token rankings, and public wallet-address PnL leaderboards across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Binance Web3 public endpoints and may include user-selected parameters. <br>
Mitigation: Avoid entering private information in query parameters and use the skill only for public market lookup workflows. <br>
Risk: Address-level leaderboard results may expose public wallet-address performance profiles. <br>
Mitigation: Do not use wallet-address data for harassment, doxxing, identity inference, or other abusive profiling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Awessh/crypto-market-rank) <br>
- [Publisher profile](https://clawhub.ai/user/Awessh) <br>
- [Social Hype Leaderboard API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/social/hype/rank/leaderboard) <br>
- [Unified Token Rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list) <br>
- [Smart Money Inflow Rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/tracker/wallet/token/inflow/rank/query) <br>
- [Meme Rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/exclusive/rank/list) <br>
- [Address PnL Rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/market/leaderboard/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public token, market, social sentiment, smart money, meme, and wallet leaderboard data returned by Binance Web3 public endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
