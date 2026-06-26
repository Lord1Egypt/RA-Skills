## Description: <br>
Enables agents to help configure and use deBridge MCP for non-custodial cross-chain crypto swaps and transfers with route discovery, fee estimates, order creation, and status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect agents to deBridge MCP so they can prepare cross-chain swap quotes, create orders after user confirmation, and monitor order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real crypto swap workflows where mistaken chain, token, amount, recipient, fee, or slippage choices can cause financial loss. <br>
Mitigation: Require explicit user review of the quote and wallet signature prompt, including chain, token, amount, recipient, fees, and slippage, and start with small test amounts. <br>
Risk: The setup flow builds remote code without pinning a reviewed commit or package versions. <br>
Mitigation: Use a reviewed and pinned source revision and dependency lockfile when supply-chain control matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/debridge-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/aviclaw) <br>
- [deBridge MCP server repository referenced by the artifact](https://github.com/debridge-finance/debridge-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide MCP-backed quote, order, chain-listing, and status workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
