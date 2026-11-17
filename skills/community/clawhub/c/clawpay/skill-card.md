## Description:

Payment requests and delivery for AI agents and humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirch](https://clawhub.ai/user/kirch)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use Clawpay to create crypto payment requests, share payment links, check payment status, and optionally deliver paid results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create crypto payment requests, and the packaged metadata includes an unsafe zero-address default recipient.

Mitigation: Require explicit user approval for each payment request and verify the final recipient wallet address, network, asset, amount, and counterparty before payment.

Risk: Delivery payloads may be sent to a third-party payment service with under-disclosed data handling.

Mitigation: Avoid sending secrets or sensitive personal data in delivery payloads and review data handling expectations before use.

Risk: Install commands fetch remote skill files without pinned versions or signature verification.

Mitigation: Prefer pinned releases and verify downloaded files against server-provided checksums or signatures before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirch/skills/clawpay)
- [Clawpay homepage](https://clawpay.ai)
- [Clawpay API base](https://clawpay.ai/v1)
- [Clawpay skill file](https://clawpay.ai/skill.md)
- [Clawpay heartbeat guide](https://clawpay.ai/heartbeat.md)
- [Clawpay skill metadata](https://clawpay.ai/skill.json)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through request creation, payment status polling, and optional delivery calls.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
