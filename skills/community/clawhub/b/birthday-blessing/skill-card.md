## Description:

Generates Chinese birthday blessing messages after a paid order and payment-verification flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub or OpenClaw users use this skill to create a paid order and receive a Chinese birthday greeting for a family member, friend, teacher, partner, or general recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags the paid payment handling as poorly scoped and inconsistent.

Mitigation: Review and fix the order creation and payment-verification flow before installation or release.

Risk: Runtime configuration includes payment recipient and cryptographic key values.

Mitigation: Confirm the real payee in the YAML config and remove or replace bundled secrets before use.

Risk: The skill declares outbound network and credential-read permissions.

Mitigation: Restrict permissions to the minimum needed, pin any clawtip dependency, and review external payment interactions.

Risk: The source text requests hidden reasoning disclosure.

Mitigation: Do not allow the skill to request or reveal hidden reasoning; keep user-facing responses limited to useful results and status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulian822/skills/birthday-blessing)
- [Publisher profile](https://clawhub.ai/user/liulian822)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status lines and Chinese blessing text, with JSON/YAML configuration for payment setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires successful payment status before producing a blessing; order records are read from the local payment flow.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
