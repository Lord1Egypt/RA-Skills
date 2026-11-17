## Description:

auto-context is an intelligent context health checker for AI coding assistants that analyzes session context pollution and recommends whether to continue, use /fork or /btw, or start a new session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding assistant users use this skill to monitor long-running sessions for context drift, noise, repeated tool use, and compression pressure, then receive concise recommendations for continuing, branching, or starting a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-mode may interrupt with context-management suggestions because trigger boundaries are not tightly specified.

Mitigation: Treat reminders as advisory and review auto-trigger behavior before enabling the skill in workflows where interruption control is important.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xcjl/skills/0xcjl-auto-context)
- [Project repository from metadata](https://github.com/0xcjl/auto-context)
- [Original skill credited by artifact documentation](https://github.com/lovstudio/skills/tree/main/skills/lovstudio-auto-context)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown health reports and concise plain-text reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual reports summarize context health and recommendations; automatic reminders are intended to be brief and advisory.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
