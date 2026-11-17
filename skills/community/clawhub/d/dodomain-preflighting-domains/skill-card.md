## Description:

Checks a domain's DNS provider, registrable zone, connection options, and existing team connections before customer onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Customer onboarding teams and developers use this skill to assess how a customer domain can be connected, identify its DNS provider, and check whether the team already has a connection without starting a session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS provider detection may be uncertain or change between checks.

Mitigation: Disclose low confidence and recheck live results before relying on connection guidance.

Risk: The doDomain connector may expose existing team connection records for the checked domain.

Mitigation: Use the connector with appropriate team authorization and share connection details only with intended recipients.

## Reference(s):

- [Preflighting Domains on ClawHub](https://clawhub.ai/devino/skills/dodomain-preflighting-domains)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes DNS provider, registrable zone, connection tier, setup steps, and any existing team connection; does not start or modify connections.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
