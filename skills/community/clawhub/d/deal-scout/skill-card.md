## Description:

Autonomous Gmail-to-CRM deal pipeline for solo operators. Classifies inbound deal emails with Gemini, logs them to a free HubSpot CRM, notifies on Discord, and sends approved replies during UK business hours. Zero hosted infrastructure; runs as a single local MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asmaiqbal01](https://clawhub.ai/user/asmaiqbal01)

### License/Terms of Use:

MIT-0

## Use Case:

Solo operators and small teams use this skill to triage Gmail deal inquiries, classify likely opportunities, log confirmed deals in HubSpot, send Discord alerts, and prepare approved Gmail replies during UK business hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks operators to install mutable proprietary code from GitHub while granting access to email and CRM credentials.

Mitigation: Review and pin a trusted commit or release before installing, test with non-production accounts first, and rotate credentials if an unreviewed revision was previously used.

Risk: The local MCP gateway can expose access to deal records, email actions, and quota information if bound too broadly or run with excessive privileges.

Mitigation: Keep the gateway bound to localhost, run it under a dedicated low-privilege account, and grant the narrowest possible Gmail and HubSpot permissions.

Risk: Development extras and optional integrations may increase local attack surface or credential exposure.

Mitigation: Avoid development extras for normal use and only enable Discord notifications with a scoped webhook when alerts are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asmaiqbal01/skills/deal-scout)
- [Project homepage](https://github.com/AsmaIqbal01/openclaw-deal-scout)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local MCP gateway setup, required credentials, Gmail-to-HubSpot workflow operation, and constraints for free-tier services.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
