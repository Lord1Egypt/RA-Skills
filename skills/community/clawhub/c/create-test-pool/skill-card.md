## Description: <br>
Deploys a custom Uniswap pool on a local testnet with configurable parameters for controlled agent and strategy testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DeFi testing teams use this skill to create local Uniswap V2 or V3 pools with chosen tokens, prices, fee tiers, liquidity, and tick ranges for controlled edge-case testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can deploy and fund mock Uniswap pools through MCP tools, so using the wrong network could affect non-test assets. <br>
Mitigation: Use only with a known local Uniswap testnet or disposable fork, and confirm the Uniswap MCP server is not pointed at a production or real-funds network before execution. <br>
Risk: Incorrect token pair, liquidity, price, fee tier, or tick range choices can create misleading test conditions. <br>
Mitigation: Confirm all requested pool parameters with the user before deployment and present the deployed pool details after creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/create-test-pool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown with pool details, suggested follow-ups, and user-facing error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Uniswap MCP tools to fund a test account, deploy a mock pool, and inspect pool state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
