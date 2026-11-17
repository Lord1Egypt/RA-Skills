## Description:

Manage OpenClaw isolated agents from chat with short commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alincatalin](https://clawhub.ai/user/alincatalin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage OpenClaw isolated agents from chat, including creating, listing, switching, binding, unbinding, deleting, and setting agent identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently create, bind, unbind, reconfigure, or delete OpenClaw agents and channel bindings from chat.

Mitigation: Install and use it only in trusted workspaces where chat-driven OpenClaw agent reconfiguration is intended and acceptable.

Risk: The helper can run an agent deletion command without enforcing the confirmation described by the skill instructions.

Mitigation: Require a matching confirmation flag or equivalent guard before invoking delete, and review delete operations before execution.

Risk: Incorrect routing or identity changes could direct a channel to the wrong agent or present an unintended agent identity.

Mitigation: Review the generated OpenClaw command, target agent name, and channel binding before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alincatalin/skills/agent-control)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit OpenClaw CLI commands and JSON-formatted helper results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
