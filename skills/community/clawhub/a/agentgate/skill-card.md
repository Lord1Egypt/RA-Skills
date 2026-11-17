## Description:

API gateway for personal data with human-in-the-loop write approval, connecting agents to GitHub, Bluesky, Google Calendar, Home Assistant, and other services through a single API with safety controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monteslu](https://clawhub.ai/user/monteslu)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure agents to access an agentgate API gateway, discover configured services, read data, submit write requests for human approval, exchange agent messages, and store or retrieve mementos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer-token access can expose personal-service access if used over plain HTTP or an untrusted network.

Mitigation: Use HTTPS or a private encrypted tunnel for non-local connections and scope the API key tightly.

Risk: Bypass mode can allow immediate writes to connected services without human approval.

Mitigation: Leave write bypass disabled unless the operator has explicitly accepted immediate changes to connected services.

Risk: The skill connects agents to personal services through an agentgate server.

Mitigation: Install only if you control the agentgate server and keep the server separated from the agent host as documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monteslu/skills/agentgate)
- [Agentgate documentation](https://agentgate.org)
- [Agentgate skills documentation](https://agentgate.org/docs/skills)
- [Agentgate GitHub repository](https://github.com/monteslu/agentgate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENT_GATE_TOKEN and AGENT_GATE_URL for the target agentgate instance.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
