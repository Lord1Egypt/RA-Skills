## Description: <br>
Enforce fine-grained spending policies before executing any payment, transfer, swap, or bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwattana](https://clawhub.ai/user/kwattana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to require Conto policy approval before an AI agent sends funds, performs swaps or bridges, or pays for x402 services. It also helps manage spending policies, limits, counterparty rules, approvals, and payment confirmations from Hermes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live payment and policy-administration authority. <br>
Mitigation: Use a Standard SDK key for routine payment checks, reserve Admin keys for short controlled policy-management sessions, start with low or testnet limits, and require explicit confirmation before any real transfer or policy deletion. <br>
Risk: Weak local confirmation and credential-storage safeguards can expose payment authority. <br>
Mitigation: Protect ~/.hermes/.env with restrictive permissions or a secret manager and avoid leaving high-privilege keys available to long-running agents. <br>
Risk: A misconfigured API endpoint could route approvals or policy operations to an untrusted service. <br>
Mitigation: Verify CONTO_API_URL points to the trusted Conto endpoint before using the skill. <br>


## Reference(s): <br>
- [Conto homepage](https://conto.finance) <br>
- [Conto Hermes on ClawHub](https://clawhub.ai/kwattana/conto-hermes) <br>
- [Conto Hermes documentation](https://conto.finance/docs/sdk/hermes) <br>
- [Well-known skill endpoint](https://conto.finance/.well-known/skills/conto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and payment-policy instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, network access to the Conto API, and a CONTO_SDK_KEY for payment and policy operations.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
