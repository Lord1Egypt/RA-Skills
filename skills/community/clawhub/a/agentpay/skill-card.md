## Description: <br>
Agentpay helps agents propose and execute real online purchases through the AgentPay CLI or MCP server while requiring human approval and keeping payment credentials out of the agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kar69-96](https://clawhub.ai/user/kar69-96) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Agentpay to prepare purchase proposals, route them for human review, and execute approved online checkouts through the AgentPay CLI or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-payment checkout access can lead to unintended purchases, excessive spend, or approval of incorrect order details. <br>
Mitigation: Use a low-limit or virtual card, set strict total and per-transaction budgets, and review merchant, item, URL, final price, shipping details, recurrence, and cancellation terms before approving. <br>
Risk: HTTP MCP exposure can make payment operations reachable outside the intended local agent session. <br>
Mitigation: Prefer stdio transport; use HTTP MCP only when it is local and authenticated. <br>
Risk: The external agentpay npm package handles sensitive payment workflows and checkout automation. <br>
Mitigation: Install only when the publisher and package are trusted, and review the package and configuration before use. <br>


## Reference(s): <br>
- [Agentpay ClawHub listing](https://clawhub.ai/kar69-96/agentpay) <br>
- [kar69-96 publisher profile](https://clawhub.ai/user/kar69-96) <br>
- [AgentPay CLI Reference](references/cli-reference.md) <br>
- [AgentPay Purchase Workflow](references/workflow.md) <br>
- [agentpay npm package](https://www.npmjs.com/package/agentpay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and MCP usage steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose real-payment transactions; requires human approval and AgentPay CLI or npx availability.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
