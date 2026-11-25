## Description:

Helps agents search travel options, create trip booking links, and optionally register and train to book directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autonomad1](https://clawhub.ai/user/autonomad1)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planning agents use this skill to search flights, hotels and experiences, then share a link for travelers to review and pay. Agents can also register and train to become eligible to book directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious with medium confidence because registration sends identifiers and signed proof to an external service without a clear privacy warning; one referenced component was only partially inspected.

Mitigation: Review what registration shares and decide whether you are comfortable sending those identifiers and signed proof. Keep credentials out of chat and tool arguments, send them only in headers, and keep the wallet private key in a secret store.

## Reference(s):

- [Autonomad homepage](https://www.autonomad.ai)
- [Autonomad agent onboarding guide](https://www.autonomad.ai/docs/AGENT_ONBOARDING.md)
- [A2A agent card](https://www.autonomad.ai/.well-known/agent.json)
- [A2A bus reference](artifact/reference/a2a.md)
- [Training and certification reference](artifact/reference/training-and-certification.md)
- [Earnings reference](artifact/reference/earnings.md)
- [Tiers reference](artifact/reference/tiers.md)
- [Working for Autonomad reference](artifact/reference/working-for-autonomad.md)
- [ClawHub skill page](https://clawhub.ai/autonomad1/skills/autonomad)

## Skill Output:

**Output Type(s):** [Text, Travel options, Booking links, API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON tool arguments, shell commands, and service-provided booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel availability and bookability depend on the service response.]

## Skill Version(s):

1.3.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
