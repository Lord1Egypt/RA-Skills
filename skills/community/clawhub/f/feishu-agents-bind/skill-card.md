## Description:

This skill helps agents bind a Feishu bot to an OpenClaw agent by collecting App ID and App Secret details, configuring the Feishu account, binding the agent, and restarting the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigcpro](https://clawhub.ai/user/aigcpro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect a Feishu bot to a selected or newly created agent, configure required credentials, and restart the gateway so the channel becomes active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App ID and App Secret values may be stored in OpenClaw configuration or exposed through command history and logs.

Mitigation: Use only credentials intended for this deployment, restrict log sharing, and rotate any secret that may have been exposed.

Risk: Unvalidated agent names could lead to unintended agent creation, binding, or configuration changes.

Mitigation: Validate agent names against a strict safe character set and confirm the target agent before applying commands.

Risk: The workflow can mutate channel configuration and restart the gateway.

Mitigation: Require explicit approval before agent creation, config mutation, binding, and gateway restart, and run status checks after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aigcpro/skills/feishu-agents-bind)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with OpenClaw shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational commands that create agents, write Feishu credentials to configuration, bind channels, restart the gateway, and check channel status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
