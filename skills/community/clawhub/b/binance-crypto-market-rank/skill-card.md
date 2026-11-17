## Description:

Crypto market rankings and leaderboards for trending tokens, Binance Alpha tokens, smart money inflows, meme token ranks, and top trader PnL leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Binance Web3 market ranking endpoints and summarize current token trends, social hype, smart money inflows, meme token ranks, and trader PnL leaderboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Binance Web3 and may surface fast-changing market ranking data.

Mitigation: Treat results as informational, cite the query context, and avoid presenting rankings as financial advice.

Risk: Leaderboard responses may include public wallet addresses, labels, balances, and trading performance.

Mitigation: Share only the details needed for the user's ranking request and avoid unnecessary lookup or redistribution of public wallet leaderboard data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dexploarer/skills/binance-crypto-market-rank)
- [Binance Web3 social hype leaderboard API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/social/hype/rank/leaderboard/ai)
- [Binance Web3 unified token rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list/ai)
- [Binance Web3 smart money inflow rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/tracker/wallet/token/inflow/rank/query/ai)
- [Binance Web3 meme rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/exclusive/rank/list/ai)
- [Binance Web3 address PnL leaderboard API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/market/leaderboard/query/ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summary with JSON API results from shell execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live Binance Web3 responses may include token metrics, public wallet addresses, labels, balances, and trading performance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
