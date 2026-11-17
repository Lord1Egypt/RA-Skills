## Description:

Provides MQTT-based commands for publishing and subscribing to agent introduction and status messages through a local broker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyunwoo91](https://clawhub.ai/user/hyunwoo91)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to publish an agent's ID, role, and current activity to MQTT topics and to subscribe to intro or status messages from one or more agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent IDs, roles, activities, and retained status messages may be visible to any client with broker access.

Mitigation: Use a trusted broker with authentication, ACLs, and TLS when crossing trust boundaries; avoid publishing sensitive roles or activities.

Risk: Checking the agent ID by printing the full OpenClaw configuration can expose unrelated local configuration details.

Mitigation: Extract only the needed agent_id instead of printing the full configuration.

Risk: Retained MQTT messages can persist outdated or sensitive agent state.

Mitigation: Define clear retained-message rules and publish only non-sensitive state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyunwoo91/skills/communication-mqtt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MQTT message text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local MQTT broker at localhost:1883 with QoS 1; published messages are retained by the broker.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
