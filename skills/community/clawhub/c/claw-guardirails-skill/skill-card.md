## Description:

Enforces guarded execution with safe_exec, safe_send, and safe_action for tasks that may run shell commands, send channel messages, or call external APIs/actions that can mutate data or state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eveiljuice](https://clawhub.ai/user/eveiljuice)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to route shell commands, outbound messages, and mutating external actions through guarded tool calls and approval handling before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may block or slow workflows if the runtime does not provide safe_exec, safe_send, and safe_action.

Mitigation: Confirm the guarded tools are available in the target environment before enabling the skill.

Risk: Commands, outbound messages, and mutating external actions can still have side effects when approved.

Mitigation: Prefer read-only or reversible operations first and require explicit approval when the resolver returns require_approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/eveiljuice/skills/claw-guardirails-skill)
- [Publisher profile](https://clawhub.ai/user/eveiljuice)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes risky execution, outbound messaging, and side-effect actions through safe_exec, safe_send, and safe_action when those tools are available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
