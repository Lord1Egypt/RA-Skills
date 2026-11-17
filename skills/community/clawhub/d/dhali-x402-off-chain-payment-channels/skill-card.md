## Description:

Helps agents manage Dhali assets and implement off-chain x402 payment flows for providers and consumers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desimmons](https://clawhub.ai/user/desimmons)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure Dhali x402 provider resource servers and consumer payment-signature flows for monetized APIs. The examples cover Python and JavaScript setup across XRPL and Ethereum/EVM-style networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Consumer examples can automatically fund a payment channel when no channel is found.

Mitigation: Require explicit confirmation before deposit calls, default to test networks, and configure spend caps before connecting a funded wallet.

Risk: Payment-channel examples can perform real financial operations.

Mitigation: Verify currency units, networks, destination asset IDs, and facilitator URLs before use.

Risk: Unpinned SDK and framework installs can change behavior over time.

Mitigation: Pin dependencies and run examples in an isolated environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/desimmons/skills/dhali-x402-off-chain-payment-channels)
- [ClawHub publisher profile](https://clawhub.ai/user/desimmons)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands and payment-channel examples for provider and consumer x402 flows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
