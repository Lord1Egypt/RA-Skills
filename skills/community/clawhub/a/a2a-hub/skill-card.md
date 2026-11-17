## Description:

Manage the MoltBot A2A Hub by registering agents, searching the registry, relaying messages, and streaming responses through the A2A agent-to-agent protocol hub deployed at a2a-hub.fly.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myrodar](https://clawhub.ai/user/myrodar)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to register A2A-compatible agents, discover registered agents, and relay or stream messages through the MoltBot A2A Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent metadata, message contents, and upstream API keys may be routed through a third-party relay at a2a-hub.fly.dev.

Mitigation: Use the skill only when that relay trust boundary is acceptable, and avoid sending sensitive content unless the workflow permits it.

Risk: A reusable upstream API key could be stored or forwarded as part of agent registration or updates.

Mitigation: Use a dedicated, tightly scoped, revocable key with spending and rate limits instead of a general-purpose or long-lived key.

Risk: Deleting an agent registration removes the hub record for that agent.

Mitigation: Confirm the target agent ID and retain any needed registration details before issuing delete requests.

## Reference(s):

- [ClawHub A2A Hub Skill](https://clawhub.ai/myrodar/skills/a2a-hub)
- [MoltBot A2A Hub Service](https://a2a-hub.fly.dev)
- [A2A Hub Skill Documentation](artifact/SKILL.md)
- [A2A Hub README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples for registering, searching, updating, deleting, sending messages, and streaming responses.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
