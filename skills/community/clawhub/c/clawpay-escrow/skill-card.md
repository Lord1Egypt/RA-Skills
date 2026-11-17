## Description:

Send and receive escrow payments on Solana using ClawPay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakemeyer125-design](https://clawhub.ai/user/jakemeyer125-design)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to create, monitor, release, refund, and verify Solana escrow payments between agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate transactions involving real Solana funds.

Mitigation: Use a dedicated low-balance wallet and require explicit confirmation of recipient, amount, network, timing windows, and fees before any transaction is signed.

Risk: The skill requires access to a Solana wallet keypair and may look in broad default locations.

Mitigation: Set SOLANA_KEYPAIR_PATH to the exact intended keypair, avoid program or deployment keys, and do not guess or search beyond user-approved paths.

Risk: The setup flow installs the clawpay SDK without pinning a package version.

Mitigation: Verify the package source and version before installation, and prefer a reviewed pinned version for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jakemeyer125-design/skills/clawpay-escrow)
- [ClawPay website](https://claw-pay.com)
- [clawpay SDK on PyPI](https://pypi.org/project/clawpay/)
- [ClawPay SDK source](https://github.com/jakemeyer125-design/ClawPay-SDK)
- [ClawPay Solana program](https://explorer.solana.com/address/F2nwkN9i2kUDgjfLwHwz2zPBXDxLDFjzmmV4TXT6BWeD)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction guidance, escrow status details, receipt checks, and Solana Explorer verification links.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
