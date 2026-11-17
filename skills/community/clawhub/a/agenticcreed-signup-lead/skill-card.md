## Description:

Create a new signup lead in AgenticCreed by submitting contact and personal details to its public HTTP API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo)

### License/Terms of Use:


## Use Case:

Agents and operators use this skill to submit consented signup lead records to AgenticCreed with required contact details and optional personal or employment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal data such as contact details, address, date of birth, WhatsApp number, and employment details.

Mitigation: Use it only with clear consent from the person whose details are submitted, and avoid sending optional personal fields unless they are required.

Risk: The skill requires an AgenticCreed API key to submit signup leads.

Mitigation: Set AGENTICCREED_API_KEY only in environments where lead submission is intended and authorized.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/waqas-orcalo/skills/agenticcreed-signup-lead)
- [AgenticCreed signup leads endpoint](https://gateway.agenticcreed.ai/signup-leads)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON API response exposed to the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTICCREED_API_KEY and lead fields supplied by the agent or user.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
