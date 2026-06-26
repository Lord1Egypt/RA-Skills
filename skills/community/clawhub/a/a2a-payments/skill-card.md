## Description: <br>
Blockchain USDC payments via APay for paying services, managing budgets, opening streaming channels, and handling x402 protocol requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Paparusi](https://clawhub.ai/user/Paparusi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to let an agent check APay balances, evaluate budgets, pay services in USDC on Base, manage streaming payment channels, and make x402 payment-backed requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real USDC and automatically pay for x402 web requests. <br>
Mitigation: Use testnet or a low-balance wallet first, set strict spending caps, and require explicit approval for every payment-capable action. <br>
Risk: The external plugin source and wallet approval model affect payment safety. <br>
Mitigation: Verify the A2A Corp plugin source and wallet approval behavior before installing or using it with funds. <br>


## Reference(s): <br>
- [A2A Payments on ClawHub](https://clawhub.ai/Paparusi/a2a-payments) <br>
- [Paparusi publisher profile](https://clawhub.ai/user/Paparusi) <br>
- [A2A Corp OpenClaw plugin](https://www.npmjs.com/package/@a2a/openclaw-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, tool calls, guidance] <br>
**Output Format:** [Markdown guidance with APay tool invocation examples and payment result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce balance, budget, service, payment receipt, streaming channel, and x402 fetch results through the APay plugin.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
