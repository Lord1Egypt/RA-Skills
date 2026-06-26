## Description: <br>
Provides OpenClaw agents with x402 payment safety protocols for validating payments, enforcing spending limits, protecting wallets, and logging transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edvisage](https://clawhub.ai/user/edvisage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give payment-enabled OpenClaw agents safety guidance for x402 transactions, including service verification, spend limits, wallet isolation, human approval thresholds, and transaction logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A funded wallet could spend beyond the user's intended limits during autonomous x402 payments. <br>
Mitigation: Use a dedicated low-balance wallet, configure strict daily and per-transaction spending limits, and require human approval above the configured threshold. <br>
Risk: Payment activity and transaction logs can expose sensitive operational or financial information. <br>
Mitigation: Decide where transaction logs and weekly summaries are stored, who receives them, and how long they are retained before enabling real transactions. <br>
Risk: An agent could pay an unapproved or spoofed service. <br>
Mitigation: Whitelist approved services and verify the service domain, amount, currency, and recipient wallet before signing a payment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/edvisage/edvisage-b2a-commerce) <br>
- [Edvisage publisher profile](https://clawhub.ai/user/edvisage) <br>
- [Edvisage Global AI tools](https://edvisageglobal.com/ai-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only safety guidance; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md; package.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
