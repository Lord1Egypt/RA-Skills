## Description: <br>
Execute Uniswap token swaps from natural-language requests with quotes, safety checks, simulation, routing, execution, and result reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare and execute Uniswap token swaps from natural-language requests. It is intended for workflows where route, fees, slippage, safety checks, transaction results, and errors need to be surfaced clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real crypto assets through an autonomous trading workflow, and the security summary notes that a clear final confirmation step is not evident. <br>
Mitigation: Use a limited wallet, review the external MCP server separately, and require a visible quote, route, chain, fees, slippage, and explicit user confirmation before any transaction is signed or submitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/execute-swap) <br>
- [Agentic-Uniswap MCP server](https://github.com/wpank/Agentic-Uniswap/tree/main/packages/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown result summaries with transaction links, route details, safety status, error messages, and suggested next actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token amounts, price impact, gas cost, slippage, chain, transaction hash, and safety-check status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
