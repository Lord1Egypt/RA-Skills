## Description:

Real-time meme token lists from Pump.fun, Four.meme and other launchpads. Use when asked about new meme tokens, trending tokens, pump.fun tokens, bonding curve, migration status, or market hot topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current meme-token rankings and market topic lists across supported Solana and BSC launchpads. It helps agents summarize new launches, migration status, holder distribution, liquidity, volume, market-cap, and topic-inflow signals from Binance Web3 APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live third-party market data that may be stale, incomplete, or unsuitable for trading decisions.

Mitigation: Treat results as informational market data, verify token details independently, and do not rely on summaries as financial advice.

Risk: Running the skill sends requests to Binance Web3 API endpoints.

Mitigation: Install and run only when live requests to Binance Web3 for token and topic rankings are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dexploarer/skills/binance-meme-rush)
- [Binance Web3 Meme Rush rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list/ai)
- [Binance Web3 Topic Rush rank API](https://web3.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list/ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Analysis, Guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live third-party market data and does not require credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
