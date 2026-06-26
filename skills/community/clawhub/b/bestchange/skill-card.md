## Description: <br>
Find trusted BestChange exchangers for crypto-to-fiat and e-currency exchange requests using the hosted BestChange MCP tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftadviser](https://clawhub.ai/user/swiftadviser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve BestChange currency codes and compare live exchanger options for crypto, fiat, and e-currency routes. It helps present ranked options while requiring users to verify final rates, networks, payout rails, and destinations before sending funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exchange lookup details are sent to the hosted MCP provider. <br>
Mitigation: Do not include wallet secrets, account credentials, private recipient details, or personal financial identifiers in prompts. <br>
Risk: Returned exchanger rankings and referral links are decision support, not a guarantee of final exchange terms. <br>
Mitigation: Verify rates, network, payout rail, reputation, reserves, and final destination directly before sending funds. <br>
Risk: If the MCP service is unavailable or currency data is missing, the agent cannot fetch live rates for the route. <br>
Mitigation: Report the unavailable service or missing currency clearly and avoid fabricating rates, reserves, exchanger names, or links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swiftadviser/bestchange) <br>
- [BestChange MCP homepage](https://bestchange-mcp.krutovoy.me) <br>
- [BestChange MCP endpoint](https://bestchange-mcp.krutovoy.me/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with exchanger summaries, setup commands, and verification guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on live BestChange API data and the hosted MCP service being connected.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
