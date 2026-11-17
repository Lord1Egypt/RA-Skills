## Description:

Adds independent, signed Fidacy verdicts to Brex CrabTrap audits, enabling publicly verifiable proof without altering CrabTrap's enforcement flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidacy](https://clawhub.ai/user/fidacy)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineering teams that already run or are evaluating Brex CrabTrap use this skill to add independently verifiable Fidacy verdicts to local agent audit decisions for vendor reviews, insurance, disputes, and regulatory questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned external adapter that handles local audit events and a Fidacy API key.

Mitigation: Use a pinned and audited adapter version, run it under a dedicated low-privilege account, and scope and rotate the Fidacy API key.

Risk: CrabTrap event data may be transmitted, logged, retained, or redacted by the external service.

Mitigation: Confirm what event data is transmitted, logged, retained, and redacted before installing or using the adapter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fidacy/skills/fidacy-crabtrap-verdicts)
- [Fidacy engine API signup](https://app.fidacy.com/signup)
- [Fidacy public JWKS](https://api.fidacy.com/.well-known/jwks.json)
- [Fidacy verifier](https://fidacy.com/verify)
- [Fidacy comparison](https://fidacy.com/comparison)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and verification guidance for pairing CrabTrap events with signed Fidacy verdicts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
