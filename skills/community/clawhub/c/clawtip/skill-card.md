## Description:

ClawTip helps agents handle ClawTip payment requests, user token creation, wallet access, registration checks, and skill information requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jd-clawtip](https://clawhub.ai/user/jd-clawtip)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and developers use this skill to complete ClawTip micro-payment workflows, create user payment tokens, view wallet entry points, and check registration status when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-related commands may be initiated from third-party skill requests.

Mitigation: Require clear per-transaction user approval before financial actions and only proceed when the request includes valid payment parameters.

Risk: The skill depends on a third-party service and npm CLI package for payment and wallet workflows.

Mitigation: Install and use it only in environments that trust ClawTip and the pinned npm package.

Risk: Payment or wallet flows can expose authorization URLs or QR-code paths during user interaction.

Mitigation: Treat those values as sensitive, avoid retaining them in logs, and run the agent with limited file, environment, and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jd-clawtip/skills/clawtip)
- [Publisher profile](https://clawhub.ai/user/jd-clawtip)
- [ClawTip website](https://clawtip.jd.com)
- [ClawTip wallet entry](https://clawtip.jd.com/qrcode?bizUrl=https://jpay.jd.com/ecnya2a/claw/index)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with inline command invocations and payment or wallet instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local MEDIA image-path references for QR-code based authorization, authentication, or wallet access.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
