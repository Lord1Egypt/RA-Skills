## Description:

Control Home Assistant devices through the agentpass security gateway, including read-only state checks and human-approved state-changing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torbenwetter](https://clawhub.ai/user/torbenwetter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to let an agent inspect Home Assistant state, history, services, logs, and configuration, and to request guarded device changes through agentpass. State-changing actions are routed through Telegram guardian approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls Home Assistant devices through a third-party CLI dependency.

Mitigation: Confirm the agentpass package source before installing and use a narrowly scoped AGENT_TOKEN.

Risk: The skill can read Home Assistant states, history, logbook entries, services, and configuration.

Mitigation: Deploy only where this level of home-automation visibility is acceptable, and scope credentials to the minimum required access.

Risk: State-changing actions can affect physical devices.

Mitigation: Keep Telegram guardian approval enabled for state changes and rely on the documented policy blocks for custom event firing and lock control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torbenwetter/skills/agentpass)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; command stdout is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing requests may block while awaiting Telegram guardian approval and can return success, denied, timeout, connection error, or invalid argument statuses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
