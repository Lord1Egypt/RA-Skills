## Description: <br>
Autonomous Coinbase integration for portfolio tracking, trading, and on-chain payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stienski](https://clawhub.ai/user/stienski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to check Coinbase balances, review portfolio values, execute trades, and initiate crypto transfers through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority over Coinbase trading and crypto transfers. <br>
Mitigation: Use restricted Coinbase API keys, avoid transfer or withdrawal permissions unless required, and keep transaction limits very low. <br>
Risk: Incorrect asset, amount, fee, network, or destination details could cause financial loss. <br>
Mitigation: Manually verify every trade or transfer detail before execution, including the destination wallet and network. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stienski/coinbase-agent) <br>
- [Publisher profile](https://clawhub.ai/user/stienski) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or text responses with balance reports, trade confirmations, and transaction hashes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may summarize live Coinbase portfolio data or confirm agent-initiated trades and transfers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
