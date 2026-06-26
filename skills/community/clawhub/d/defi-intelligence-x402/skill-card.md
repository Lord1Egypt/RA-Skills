## Description: <br>
16-tool DeFi intelligence agent for token prices, swap quotes, wallet analytics, portfolio tracking, DeFi positions, gas oracle, ENS resolution, and contract reads via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to query DeFi market data, wallet activity, portfolio exposure, swap quotes, and contract reads through a paid x402 gateway. The skill also exposes wallet-affecting write operations, so operational use should include explicit review before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends wallet-related data and an API key to a paid external gateway. <br>
Mitigation: Install only if the gateway operator is trusted, scope and rotate the API key, and avoid submitting wallet data that should not leave the operating environment. <br>
Risk: Write endpoints can initiate irreversible wallet-affecting actions such as swaps or contract writes. <br>
Mitigation: Require explicit human approval before any write call and verify chain, recipient, token amounts, allowances, and slippage out of band. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plagtech/defi-intelligence-x402) <br>
- [x402 gateway](https://gateway.spraay.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEARCH_API_KEY, curl, and python3; RESEARCH_GATEWAY_URL is optional and defaults to the x402 gateway. Endpoint calls may incur USDC micropayment costs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
