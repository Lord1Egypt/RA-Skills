## Description: <br>
Query Bifrost SLPx liquid staking protocol data on Ethereum, Base, Optimism, and Arbitrum, including vETH/ETH exchange rates, APY, TVL, user balances, redemption queue status, and protocol stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ark930](https://clawhub.ai/user/ark930) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and DeFi analysts use this skill to query Bifrost vETH rates, yields, protocol statistics, balances, and withdrawal status from read-only on-chain calls and the Bifrost REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial decisions may be affected by stale or incorrect protocol data, RPC responses, or contract endpoint assumptions. <br>
Mitigation: Verify the Bifrost contract address and API endpoint against official sources before relying on results for financial decisions. <br>
Risk: Wallet-address lookups can expose address interest or usage patterns to an RPC provider. <br>
Mitigation: Use a trusted RPC provider when wallet-address privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ark930/bifrost-slpx-info) <br>
- [Bifrost vETH page](https://www.bifrost.io/vtoken/veth) <br>
- [Bifrost vETH app](https://app.bifrost.io/vstaking/vETH) <br>
- [Bifrost site API](https://api.bifrost.app/api/site) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-RPC examples, decoded numeric results, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only responses should use fresh RPC or API data and convert wei values to human-readable ETH or vETH amounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
