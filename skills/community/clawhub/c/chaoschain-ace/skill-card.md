## Description:

Authorize autonomous x402 API payments with bounded, wallet-funded session keys under strict policy limits in ACE Phase 0 without credit lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumeetchougule](https://clawhub.ai/user/sumeetchougule)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when an agent needs to call x402-gated APIs with explicit spend limits, allowed categories, and short-lived wallet-funded session keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent bounded authority to make x402 API payments.

Mitigation: Set conservative per-transaction and daily limits, require short TTLs, and restrict allowed categories to compute, data, and api before enabling payments.

Risk: Runtime dependency changes could affect payment behavior.

Mitigation: Pin the ACE SDK and ethers dependencies to exact reviewed versions before using them in runtime code.

Risk: A request may fall outside the intended payment scope or configured policy.

Mitigation: Use the skill only for x402-gated API calls, require schema discovery when parameters are unclear, and refuse P2P transfers, swaps, speculation, arbitrary wallet movement, or out-of-policy requests.

## Reference(s):

- [ChaosChain ACE SDK homepage](https://github.com/chaoschain-labs/chaoschain-ace-sdk)
- [ClawHub skill page](https://clawhub.ai/sumeetchougule/skills/chaoschain-ace)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes policy initialization, spend-reasoning, schema-discovery, and refusal guidance; it does not execute integration code itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
