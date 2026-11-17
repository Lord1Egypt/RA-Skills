## Description:

Discover events and hubs, manage branding, CheckIn venues, bracelets, wallets, and NFT tickets on the Belong platform

This skill is ready for commercial/non-commercial use.

## Publisher:

[belong](https://clawhub.ai/user/belong)

### License/Terms of Use:

MIT-0

## Use Case:

Belong attendees and event organizers use the skill to discover events and hubs, manage tickets and check-ins, and administer events, communities, and venue features on Belong.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, refund, publishing, and venue-setting operations can change account or event state.

Mitigation: Review the proposed operation and approve these changes deliberately.

Risk: Email codes, request parameters, and the saved account key are sent to the configured service.

Mitigation: Link only the intended Belong account and protect its saved key.

Risk: An endpoint override can change where account information and requests are sent; remote authorization and autonomy safeguards were not independently verified.

Mitigation: Use only trusted HTTPS endpoint overrides and review authorization safeguards before relying on autonomous actions.

## Reference(s):

- [Belong Events on ClawHub](https://clawhub.ai/belong/skills/belong-events)
- [Belong Events API endpoint](https://join.belong.net/functions/v1/openclaw-skill-proxy)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON tool responses with optional concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the requested Belong Events operation.]

## Skill Version(s):

1.8.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
