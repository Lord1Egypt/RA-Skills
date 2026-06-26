## Description: <br>
Trustless token swaps for AI agents on Base, either by relaying agent-signed CoW Protocol orders for batch-auction settlement or by creating a 1:1 on-chain escrow for human OTC trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agora0x](https://clawhub.ai/user/agora0x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to request Base token quotes, prepare locally signed CoW Protocol swap orders, submit signed orders, and check escrow or order status. It is suited to token-swap workflows that require explicit wallet control and review before signing or submitting transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create escrow trades and submit signed market orders. <br>
Mitigation: Require explicit human approval before any trade, escrow, token approval, or signed-order submission. <br>
Risk: A signed order or approval could target the wrong chain, token, amount, fee, recipient, expiry, or approval address. <br>
Mitigation: Verify chain, token addresses, amounts, fee, recipient, order expiry, and approval target before signing. <br>
Risk: Autonomous use of execute_trade or submit_signed_trade can move assets without adequate review. <br>
Mitigation: Do not allow autonomous agents to call execute_trade or submit_signed_trade without strict limits and confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agora0x/floor-otc) <br>
- [Publisher Profile](https://clawhub.ai/user/agora0x) <br>
- [Homepage](https://floor-otc.vercel.app) <br>
- [Agent Card](https://floor-a2a-production.up.railway.app/.well-known/agent.json) <br>
- [A2A JSON-RPC Endpoint](https://floor-a2a-production.up.railway.app/a2a) <br>
- [MCP SSE Endpoint](https://zesty-solace-production-13de.up.railway.app/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include quotes, EIP-712 typed data, appData, preflight balance and allowance checks, transaction or order identifiers, explorer URLs, and status summaries.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
