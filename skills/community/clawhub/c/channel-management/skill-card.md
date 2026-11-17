## Description:

Manage multiple communication channels, admin identity recognition, and primary channel configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montycn](https://clawhub.ai/user/montycn)

### License/Terms of Use:

MIT-0

## Use Case:

Managers and OpenClaw operators use this skill to identify administrators and trusted contacts across messaging channels, maintain a primary notification channel, and route escalation messages to the administrator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct-message senders may receive administrator-level trust if the deployment's allowlist is not tightly controlled.

Mitigation: Install only where direct-message ingress is restricted to the administrator, and verify administrator identity explicitly for each channel before allowing privileged actions.

Risk: The skill uses broad full-trust language for recognized administrators.

Mitigation: Keep normal approval and authorization checks for sensitive or irreversible operations, and scope the skill to channel-management workflows.

Risk: Primary-channel and trusted-contact state files affect who receives notifications and who can interact with the agent.

Mitigation: Protect the state files with appropriate filesystem permissions and review changes to primary-channel and trusted-contact configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/montycn/skills/channel-management)
- [Publisher profile](https://clawhub.ai/user/montycn)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for identity recognition, trusted-contact handling, primary-channel state, and cross-channel escalation.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
