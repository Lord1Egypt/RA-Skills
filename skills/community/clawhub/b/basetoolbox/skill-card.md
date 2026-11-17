## Description:

Checks and simulates Uniswap v3 swaps on Base before signing, with allowance, gas, token price, ENS, transaction explanation, and transfer-check support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cartonpliant](https://clawhub.ai/user/cartonpliant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, wallet operators, and agent users use this skill to preflight Base swaps, check allowances or transfers, resolve ENS, and inspect gas or token price data before signing. It is intended to keep payment, allowance, and transaction authorization steps explicit and separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet, token, recipient, calldata, or ENS fields sent to the remote API may be visible to the API operator and PayAI.

Mitigation: Show the endpoint, purpose, price, recipient, facilitator, and exact fields before each paid request, and avoid adding extra identifiers.

Risk: An HTTP 402 payment offer could be mistaken for spend authorization.

Mitigation: Require a fresh affirmative confirmation for the exact offer before payment or retry; silence, ambiguity, timeout, or unavailable confirmation means no.

Risk: Remote calldata or allowance advice could be incorrect or unsafe.

Mitigation: Treat remote calldata as untrusted, run local approval verification before allowance changes, never approve uint256.max, and require a separate human confirmation before signing or submitting any transaction.

## Reference(s):

- [Base Toolbox ClawHub Skill Page](https://clawhub.ai/cartonpliant/skills/basetoolbox)
- [Base Toolbox API Origin](https://basetoolbox.cartonpliant.workers.dev)
- [PayAI Facilitator](https://facilitator.payai.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact payment-offer details, endpoint fields, local approval verification steps, and explicit stop conditions before user authorization.]

## Skill Version(s):

1.3.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
