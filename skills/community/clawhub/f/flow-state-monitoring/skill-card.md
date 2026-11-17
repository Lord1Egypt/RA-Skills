## Description:

Workflow-driven skill that infers deep focus and autonomously mutes interruptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to detect deep-focus activity and update Google Workspace calendar availability so interruptions are muted during flow state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Google Calendar busy events automatically using configured Google Workspace access based on vague focus signals.

Mitigation: Require explicit user consent before event creation and use defined event duration, cooldowns, logging, and an easy deletion path for created events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/flow-state-monitoring)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, API Calls, Guidance]

**Output Format:** [JSON confirmation with agent guidance and shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and configured Google Workspace access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
