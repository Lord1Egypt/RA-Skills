## Description:

Reference client for paying x402 (USDC/EVM) and L402 (Lightning) HTTP 402 paywalls, detecting payment requirements, signing or settling payments only with explicitly provided credentials and spending ceilings, and retrying requests with proof of payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and access HTTP 402 paywalled APIs that support x402 or L402 payment flows. It is intended for explicit-consent payment workflows where callers provide their own credentials and spending ceilings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lightning auto-pay may expose credentials or spend beyond the stated limit.

Mitigation: Keep L402 auto-pay disabled unless BOLT11 invoice amount verification, transport verification or certificate pinning, and ceiling validation are confirmed.

Risk: Using the skill with real funds can increase financial exposure if credentials or dependencies are not constrained.

Mitigation: Use narrowly scoped macaroons, keep only small balances available, and pin and audit dependencies before deployment.

Risk: This release is reference-grade rather than production-safe payment infrastructure.

Mitigation: Review the implementation and security guidance before installing it in workflows that can spend real funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/welove111/skills/agent-pay-client)
- [Publisher Profile](https://clawhub.ai/user/welove111)
- [Publisher Homepage](https://btc-vision.org)
- [x402 Specification](https://x402.org)
- [L402 Documentation](https://docs.lightning.engineering/the-lightning-network/l402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe payment requirements, return structured payment results, or provide manual Lightning payment details depending on caller configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
