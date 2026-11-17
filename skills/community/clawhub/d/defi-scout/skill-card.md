## Description:

On-chain DeFi intelligence for AI agents across Optimism and Base, covering wallet balances, token prices, DEX estimates, yield opportunities, protocol TVL, gas prices, bridge quotes, Aave positions, and market sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[old-greggyboy](https://clawhub.ai/user/old-greggyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve live DeFi market, wallet, bridge, lending, and gas information for Optimism and Base. It supports planning and analysis workflows, not transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and query details are sent to public blockchain, bridge, and market-data APIs.

Mitigation: Use only wallet addresses and query details that are acceptable to disclose to those services.

Risk: The security evidence reports that the skill reads a shared .env file and writes cache data outside the skill directory.

Mitigation: Avoid placing unrelated secrets in the shared .env reachable by this skill, and prefer a version that reads only CMC_API_KEY and uses a skill-local or explicitly configured cache directory.

Risk: Swap output is a price-based estimate rather than an executable protocol-routed quote.

Mitigation: Use swap estimates for planning only and verify executable quotes in the relevant protocol interface before any transaction.

Risk: High APY pools and low-liquidity pools can be misleading or short-lived.

Mitigation: Filter out pools below the documented TVL threshold, flag APY above 100% as high risk, and compare gas cost to position size before presenting an opportunity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/old-greggyboy/skills/defi-scout)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price)
- [DeFiLlama yields API](https://yields.llama.fi/pools)
- [Optimism public RPC](https://mainnet.optimism.io)
- [Base public RPC](https://mainnet.base.org)
- [Across suggested fees API](https://app.across.to/api/suggested-fees)
- [CoinMarketCap API endpoints](https://pro-api.coinmarketcap.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most scripts output JSON; cmc-sentiment.js emits concise sentiment text and requires CMC_API_KEY.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
