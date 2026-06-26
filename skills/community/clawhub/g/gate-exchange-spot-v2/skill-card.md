## Description: <br>
Gate spot trading and account operations skill. Use when the user asks to buy/sell crypto on spot, check account value, or place conditional/trigger orders. Triggers on 'buy coin', 'sell spot', 'take profit', 'stop loss', or 'cancel order'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users and operators use this skill to check spot balances, draft buy and sell orders, manage open orders, place conditional trigger orders, and verify fills through a configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place, amend, and cancel real Gate spot orders. <br>
Mitigation: Use a dedicated Gate API key without withdrawal permission, verify the Gate MCP server source, and review every order draft before confirming execution. <br>
Risk: Conflicting TP/SL wording and broad activation phrases could cause misunderstanding about when trigger orders are supported. <br>
Mitigation: Resolve the TP/SL wording before release and require explicit, immediate confirmation for each trigger order or multi-leg action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-spot-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/gate-exchange) <br>
- [Skill Homepage](https://github.com/gate/gate-skills) <br>
- [Gate Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate MCP Execution Specification](references/mcp.md) <br>
- [Gate Spot Trading Scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with order drafts, status reports, confirmation prompts, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write-capable spot actions require an explicit user confirmation immediately before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
