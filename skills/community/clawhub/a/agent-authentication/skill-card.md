## Description:

Registers a new Openclaw AI Agent via the AgentAuthentication API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingdestinythe1st](https://clawhub.ai/user/kingdestinythe1st)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provision Openclaw AI agent accounts by collecting required identity and contact fields, preparing a strict JSON payload, submitting it to the AgentAuthentication API, and interpreting the response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to collect or generate account passwords and personal contact data before sending registration data to a live production endpoint.

Mitigation: Require clear user confirmation before submission, use a secure form or structured HTTP tool where available, and avoid logging passwords or full request bodies.

Risk: Server security evidence flags the release as suspicious because safe-handling and consent instructions are not explicit.

Mitigation: Review the skill before installation and add local operating procedures for credential handling, consent, and response review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingdestinythe1st/skills/agent-authentication)
- [AgentAuthentication registration endpoint](https://us-central1-openclaw-authentication-646b0.cloudfunctions.net/api/v1/agents/register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated account passwords and user contact fields; avoid logging secrets or full request bodies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
