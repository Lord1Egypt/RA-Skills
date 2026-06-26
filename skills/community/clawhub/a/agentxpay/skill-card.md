## Description: <br>
AgentXPay lets AI agents discover, pay for, subscribe to, and escrow AI services on Monad using the x402 payment protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonRUAN](https://clawhub.ai/user/JasonRUAN) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use AgentXPay to let agents discover and pay for Monad-hosted AI services, manage funded wallets, subscribe to services, and create escrow-backed jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend funds from a configured blockchain wallet. <br>
Mitigation: Use a testnet or low-balance wallet first, set strict spend limits, and require human confirmation before payment, transfer, subscription, escrow, or authorization changes. <br>
Risk: The skill can call external service URLs and may send prompts, headers, or request bodies to providers. <br>
Mitigation: Restrict allowed service endpoints and do not send sensitive prompts, secrets, or headers to untrusted provider URLs. <br>
Risk: Security review found broad spending and external-call capability without strong built-in approval or allowlist controls. <br>
Mitigation: Deploy with external approval gates, endpoint allowlists, and budget controls appropriate to the funded wallet. <br>


## Reference(s): <br>
- [AgentXPay SDK API reference](references/sdk-api.md) <br>
- [x402 protocol reference](references/x402-protocol.md) <br>
- [AgentXPay project homepage](https://github.com/AgentXPay) <br>
- [x402 protocol website](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON tool results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service listings, external AI service responses, wallet addresses, payment amounts, service identifiers, and blockchain transaction hashes.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
