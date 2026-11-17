## Description:

Model routing strategy for a multi-model AI fleet. Use when spawning sub-agents, choosing models for scheduled jobs, delegating coding tasks, or deciding which model should handle a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent builders use this skill to choose an appropriate model class for delegation, scheduled jobs, coding work, long-context analysis, and image or video tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation could influence model routing in tasks where a narrower policy is preferred.

Mitigation: Review the advisory routing guidance before installation and narrow the activation description if only explicit multi-model routing decisions should trigger it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jarvis-drakon/skills/fleet-doctrine)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory model-routing recommendations; no tool calls or files are produced by the skill itself.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
