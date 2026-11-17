## Description:

度小满支付技能 helps agents handle unpaid or insufficient-balance service responses by showing product details, generating a payment QR code for a validated payment URL, and supporting paid skill installation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duxiaoman](https://clawhub.ai/user/duxiaoman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to present payment details and QR codes when a ClawHub service is unpaid or has insufficient balance. It can also register a local client and install paid skills after payment through the publisher service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register a local client and store a signing key.

Mitigation: Review before installing and prefer versions that store credentials with owner-only permissions.

Risk: The skill can download remote ZIP packages and install files into the shared skills workspace.

Mitigation: Use only if the dxmpay/clawpay service and package-signing pipeline are trusted; prefer versions that validate skill IDs, install only into an isolated expected directory, and prevent overwrites without explicit consent.

Risk: The authoritative scan verdict is suspicious because installation behavior is broad and under-scoped for automatic approval.

Mitigation: Require human review before deployment and scan the skill before use in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duxiaoman/skills/dxm-claw-pay)
- [duxiaoman publisher profile](https://clawhub.ai/user/duxiaoman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON status from helper scripts and QR code image file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local client configuration, temporary QR code images, downloaded ZIP files, and installed skill files during guided workflows.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
