## Description: <br>
Monitor and analyze DeFi positions across protocols and chains, including LP positions, staking rewards, yield farming returns, impermanent loss calculations, and cost basis per position. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and treasury operators use this skill to collect read-only DeFi position data, calculate LP and staking performance, and prepare structured portfolio, tax, or dashboard outputs. It is intended for analysis and reporting, not for executing transactions or moving assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, DeFi positions, and tax-related financial data can be exposed to third-party analytics, RPC, and API providers. <br>
Mitigation: Use dedicated read-only and revocable API keys, limit wallet data shared with providers, and avoid submitting seed phrases or private keys. <br>
Risk: Tax and portfolio exports may contain sensitive financial records or require human review before downstream use. <br>
Mitigation: Review generated tax exports and portfolio summaries before sharing them with another agent, service, accountant, or dashboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/defi-position-tracker) <br>
- [DeBank Pro API](https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id=0xYOUR_WALLET&chain_ids=eth,arb,op,base,matic) <br>
- [Zapper balances API](https://api.zapper.xyz/v2/balances) <br>
- [Revert Finance position analytics API](https://api.revert.finance/v1/position?position_id=YOUR_NFT_ID&chain_id=1) <br>
- [The Graph Lido subgraph](https://api.thegraph.com/subgraphs/name/lidofinance/lido) <br>
- [The Graph Aave v3 subgraph](https://api.thegraph.com/subgraphs/name/aave/protocol-v3) <br>
- [Moralis DeFi positions API](https://deep-index.moralis.io/api/v2.2/0xYOUR_WALLET/defi/positions?chain=eth) <br>
- [Alchemy Ethereum RPC example](https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, and JSON schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only portfolio analysis patterns and structured DeFi position data for reporting, tax handoff, and dashboards.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
