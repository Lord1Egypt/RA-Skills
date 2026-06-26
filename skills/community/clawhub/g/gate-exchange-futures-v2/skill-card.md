## Description: <br>
Gate Exchange USDT perpetual futures trading skill. Use when the user wants to trade contracts, open/close perpetual positions, or manage futures leverage. Triggers on 'open long', 'close short', 'USDT perpetual', 'futures TP/SL'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to route Gate USDT perpetual futures requests into guarded workflows for opening, closing, amending, cancelling, and managing price-triggered orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place, amend, cancel, and close real Gate futures orders. <br>
Mitigation: Require explicit confirmation after reviewing contract, side, size, leverage, margin mode, order type, price, and affected scope before any write operation. <br>
Risk: Ambiguous trading prompts such as 'cancel all' or 'close half' can affect unintended orders or positions. <br>
Mitigation: Clarify the account, contract, position side, size, and order scope before executing broad or partial actions. <br>
Risk: The skill depends on trusted Gate MCP server behavior and externally referenced runtime rules. <br>
Mitigation: Install only from trusted Gate sources, keep API permissions narrow, and review the runtime rules before enabling live trading access. <br>


## Reference(s): <br>
- [Gate Futures MCP Specification](references/mcp.md) <br>
- [Gate Futures Open Position](references/open-position.md) <br>
- [Gate Futures Close Position](references/close-position.md) <br>
- [Gate Futures Cancel Order](references/cancel-order.md) <br>
- [Gate Futures Amend Order](references/amend-order.md) <br>
- [Gate Futures Take Profit / Stop Loss](references/tp-sl.md) <br>
- [Gate Futures Conditional Open Order](references/conditional.md) <br>
- [Gate Futures Price-Triggered Orders Manage](references/manage.md) <br>
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown guidance with MCP tool calls and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces order summaries, clarification prompts, confirmation requests, and short operation reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
