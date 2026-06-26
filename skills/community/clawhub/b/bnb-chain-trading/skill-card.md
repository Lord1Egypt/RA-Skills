## Description: <br>
Agent trading on BNB Chain. Limit, DCA, stop-loss & take-profit. Non-custodial, zero fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn-orbs](https://clawhub.ai/user/shawn-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to translate trading intent into Spot advanced swap order parameters, EIP-712 typed data, wallet approval guidance, signed relay payloads, query flows, and cancellation steps for supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The BNB-focused presentation may understate that the skill supports multiple EVM chains and can guide wallet approvals beyond BNB Chain. <br>
Mitigation: Before signing, verify the intended chain ID, adapter, token addresses, spender or verifying contract, and recipient against the supported-chain list. <br>
Risk: Approvals and signed orders can authorize token movement according to max amount, slippage, deadline, recurrence, and output constraints. <br>
Mitigation: Use wallet confirmations carefully, prefer exact approvals for the intended max amount, and review max amount, slippage, deadline, epoch, and trigger fields before signing. <br>
Risk: Relay submission shares signed trading instructions with an external service. <br>
Mitigation: Submit only the final intended signed payload, preserve the exact typed data and signature for retries or cancellation, and use onchain cancellation or approval revocation tools when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shawn-orbs/bnb-chain-trading) <br>
- [Quickstart](references/quickstart.md) <br>
- [Parameter Reference](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit Typed Data Template](assets/repermit.template.json) <br>
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>
- [Spot Chain Configuration](https://github.com/orbs-network/spot/blob/master/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces locally assembled order parameters, typed-data payloads, approval guidance, signed relay submission payloads, query instructions, and cancellation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; package.json reports 2.5.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
