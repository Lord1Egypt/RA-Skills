## Description:

Connect to 100+ third-party APIs through Maton's managed OAuth gateway for native API access from an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andre-thedev](https://clawhub.ai/user/andre-thedev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call supported business, productivity, analytics, messaging, storage, and CRM APIs through a single gateway after the user grants the needed OAuth connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send raw write or delete requests to many connected services.

Mitigation: Require explicit user confirmation before delete, financial, admin, public-posting, permission-changing, or bulk-update actions.

Risk: The gateway depends on a Maton API key and user-authorized OAuth connections.

Mitigation: Connect only required services and scopes, avoid exposing MATON_API_KEY or unredacted connection responses, and rotate the key if it appears in logs or transcripts.

Risk: Access is mediated by a third-party API gateway provider.

Mitigation: Use the skill only when the operator trusts Maton and has reviewed the connected service scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andre-thedev/skills/api-gateway-1-0-70)
- [Maton homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [Provider routing guides](references/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized OAuth connections for target services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
