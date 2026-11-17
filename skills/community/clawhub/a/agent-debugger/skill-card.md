## Description:

Agent Debugger helps developers systematically diagnose and fix AI agent issues such as tool failures, infinite loops, context overflow, rate limits, and performance bottlenecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug misbehaving AI agents, isolate failure modes, and choose fixes for loops, tool errors, context limits, rate limits, memory issues, permission failures, and performance bottlenecks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance to expose hidden or internal reasoning can disclose protected system behavior or sensitive prompt context.

Mitigation: Do not enable hidden/internal reasoning visibility; rely on visible logs, traces, and user-approved diagnostics.

Risk: Memory or tool-policy changes can persist unwanted behavior or broaden agent permissions.

Mitigation: Apply memory and tool-policy updates only with explicit user intent, narrow scope, and review before deployment.

Risk: Debugging recommendations may be incorrect for a specific agent environment.

Mitigation: Review proposed code, command, and configuration changes against local tool schemas and sandbox policies before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with diagnostic steps, checklists, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested fixes and prevention tips; proposed changes should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
