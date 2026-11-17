## Description:

00 Action Guard directs an agent to check a permission gate before using tools or taking other non-chat actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rancho718](https://clawhub.ai/user/rancho718)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this always-on OpenClaw skill to document a permission-check protocol before tool-backed actions, writes, sensitive queries, cross-platform messages, or skill execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly attempts to control nearly all tool-backed work through an undefined permission gate.

Mitigation: Install only in a controlled OpenClaw environment where the permission gate is trusted, audited, and has documented authentication, scope, timeout, and recovery behavior.

Risk: Incorrect gate behavior could block legitimate work or allow actions without an appropriate permission decision.

Mitigation: Test the gate in a non-production environment and review audit logs before enabling the skill for routine tool use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rancho718/skills/00-action-guard)
- [Publisher profile](https://clawhub.ai/user/rancho718)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown instructions and decision flow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always-on behavioral guidance for OpenClaw agents]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
