## Description: <br>
On-chain DeFi intelligence for AI agents covering wallet balances, token prices, DEX estimates, yield opportunities, protocol TVL, gas prices, and airdrop farming on Optimism and Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[old-greggyboy](https://clawhub.ai/user/old-greggyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather live DeFi market and wallet context on Optimism and Base before planning swaps, bridge moves, yield scans, or Aave health checks. Treat the outputs as informational context, not as execution advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet, market, swap, bridge, yield, and liquidation outputs may be stale, incomplete, or unsuitable for direct execution. <br>
Mitigation: Use the skill for informational analysis only and verify results with official protocol interfaces or trusted market data before taking financial action. <br>
Risk: Wallet lookups send public wallet addresses to external RPC and API providers. <br>
Mitigation: Avoid private wallet analysis unless the user is comfortable sharing the public address with those providers. <br>
Risk: Live RPC and API dependencies can time out or become temporarily unavailable. <br>
Mitigation: Retry transient failures once and clearly report unavailable data instead of filling gaps with guesses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/old-greggyboy/defi-scout) <br>
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price) <br>
- [DeFiLlama yields API](https://yields.llama.fi/pools) <br>
- [Across suggested fees API](https://app.across.to/api/suggested-fees) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON or concise text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Most scripts require no API key; CoinMarketCap sentiment requires CMC_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
