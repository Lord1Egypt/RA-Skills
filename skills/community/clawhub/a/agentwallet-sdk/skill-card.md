## Description: <br>
Non-custodial wallet SDK guidance for autonomous AI agents that need x402 payments, CCTP V2 bridge transfers, ERC-8004 identity, and Uniswap V3 swaps without server-side key custody. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[up2itnow](https://clawhub.ai/user/up2itnow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to integrate non-custodial wallet operations into AI agents, including wallet setup, payments, bridging, swaps, identity registration, and transaction signing. It is intended for agents that may interact with crypto wallets and therefore need explicit controls around keys, balances, and approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable autonomous crypto transfers, swaps, bridges, and private-key signing without clear approval or spending controls. <br>
Mitigation: Use a dedicated low-balance or restricted wallet and require explicit confirmation before every transfer, payment, bridge, swap, or signing action. <br>
Risk: Using a main wallet private key or broad wallet permissions can expose funds if an agent behaves unexpectedly or is prompted maliciously. <br>
Mitigation: Never use a main wallet private key; scope keys and permissions to the specific agent workflow. <br>
Risk: Exposing wallet operations through MCP can allow unintended agents to call payment or transaction tools. <br>
Mitigation: Avoid MCP exposure unless access can be tightly restricted to trusted agents. <br>
Risk: Unverified package installation can introduce supply-chain risk for wallet and payment operations. <br>
Mitigation: Pin and verify npm packages before installation. <br>


## Reference(s): <br>
- [Agentwallet Sdk on ClawHub](https://clawhub.ai/up2itnow/agentwallet-sdk) <br>
- [agentwallet-sdk npm package](https://www.npmjs.com/package/agentwallet-sdk) <br>
- [@agent-wallet/mastra-plugin npm package](https://www.npmjs.com/package/@agent-wallet/mastra-plugin) <br>
- [clawpay-mcp npm package](https://www.npmjs.com/package/clawpay-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet setup and transaction-related commands that require explicit user confirmation before any transfer, payment, bridge, swap, or signing action.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact/skill.json lists 1.0.0 and artifact/SKILL.md references npm v2.4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
