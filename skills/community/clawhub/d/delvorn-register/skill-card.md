## Description:

Guides agents through a $0.05 USDC payment on Base to access a Delvorn test asset and verify its public receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mranderson323](https://clawhub.ai/user/mranderson323)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to request a paid Delvorn test asset, complete the USDC payment, and check access and the public receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undeclared scripts can use a local Telegraph credential to edit a live page and republish marketplace metadata.

Mitigation: Review before installing; require the publisher to remove or fully disclose the scripts, restrict credential and network access, and require confirmation before external edits.

Risk: Access entails an external USDC payment.

Mitigation: Require explicit confirmation before payment, and do not grant access to a funded wallet without understanding the side effects.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mranderson323/skills/delvorn-register)
- [Delvorn x402 discovery](https://delvorn.site/.well-known/x402)
- [Delvorn registration writeup](https://telegra.ph/Delvorn-register-1-test-public-receipt-08-26)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Text with HTTP request steps and receipt confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Access requires a $0.05 USDC payment on Base.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
