## Description:

Context window is near capacity, causing the model to drop earlier content silently and produce degraded, partial, or inconsistent output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to recognize when a long agent conversation is losing earlier context and to choose practical next steps such as splitting work, summarizing prior material, or starting a fresh session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the skill's guidance for an automated fix for context-window limits.

Mitigation: Treat the output as workflow advice and manually decide when to split tasks, summarize context, or start a fresh session.

Risk: Long conversations can still omit or distort earlier requirements after the skill identifies near-overflow symptoms.

Mitigation: Re-inject only the current step's necessary instructions and source material before asking the agent to continue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/context-near-overflow)
- [Publisher profile](https://clawhub.ai/user/mvogt99)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file changes, system setting changes, or data persistence are requested by the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
