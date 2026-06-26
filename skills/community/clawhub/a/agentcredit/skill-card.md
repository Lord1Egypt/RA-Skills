## Description: <br>
Agentcredit helps agents request and repay small USDC microloans on Base mainnet and use AgentCredit as an x402 facilitator for payment settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbpin](https://clawhub.ai/user/jbpin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to give an agent controlled access to Base USDC microloans for x402 payments, API calls, on-chain operations, or other short-term liquidity needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real USDC debt when connected to an agent wallet and used for AgentCredit microloans or x402 settlement. <br>
Mitigation: Use test amounts first, monitor outstanding loans and fees, and install it only when an agent is intended to borrow USDC through AgentCredit. <br>
Risk: Wallet signing and payment authority could allow an agent to request loans, settle payments, or sign transactions beyond the operator's intent. <br>
Mitigation: Use wallet spending controls, keep signing authority scoped to the intended wallet and actions, and avoid unrestricted signing or payment access. <br>
Risk: Facilitator mode may make borrowing part of payment settlement without a separate loan-request interruption. <br>
Mitigation: Treat facilitator mode as borrowing, verify wallet exposure limits before use, and monitor repayments so overdue loans do not block later settlements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jbpin/agentcredit) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jbpin) <br>
- [AgentCredit API](https://agentlending.spekn.com) <br>
- [AgentCredit full agent docs](https://agentlending.spekn.com/llms-full.txt) <br>
- [AgentCredit x402 discovery](https://agentlending.spekn.com/.well-known/x402.json) <br>
- [AgentCredit A2A agent card](https://agentlending.spekn.com/.well-known/agent-card.json) <br>
- [AgentCredit pool wallet on BaseScan](https://basescan.org/address/0x510a64F194CB6196d34C93717d88f13aCF0C979f) <br>
- [Base USDC contract on BaseScan](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) <br>
- [Spekn operator site](https://spekn.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, TypeScript examples, REST endpoints, MCP configuration, and wallet-signing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce loan, credit, repayment, x402 facilitator, and wallet-signature guidance; agent actions can involve real USDC transactions and debt.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
