## Description: <br>
Edge.Trade provides on-chain trading data and order management for token research, pair inspection, wallet analysis, orders, and price alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lexomis](https://clawhub.ai/user/lexomis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Edge.Trade for crypto token discovery, pair metrics, wallet and portfolio analysis, price alerts, and order management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place orders, cancel orders, manage wallet-related flows, and subscribe to alerts through a real crypto trading integration. <br>
Mitigation: Use a limited API key where possible and require manual confirmation before every order, cancellation, strategy, wallet-management action, or alert subscription. <br>
Risk: The skill requires sensitive Edge.Trade API credentials. <br>
Mitigation: Store the API key only in a secret configuration path and avoid exposing it in prompts, logs, or generated examples. <br>
Risk: The security verdict is suspicious because consent boundaries for trading and wallet actions are not clear. <br>
Mitigation: Install only for intentional Edge.Trade crypto workflows and avoid invoking it for general investing education or casual token questions. <br>


## Reference(s): <br>
- [Edge.Trade ClawHub page](https://clawhub.ai/lexomis/edge) <br>
- [Edge.Trade agent documentation](https://edge-trade.gitbook.io/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tool, configuration, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce trading workflow guidance and MCP tool invocation instructions that require sensitive API credentials.] <br>

## Skill Version(s): <br>
v4478.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
