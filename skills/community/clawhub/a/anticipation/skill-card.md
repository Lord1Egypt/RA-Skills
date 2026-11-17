## Description:

Recognizes patterns from user history and session context so an agent can offer proactive, context-aware help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcben90](https://clawhub.ai/user/mcben90)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent toward proactive assistance based on repeated conversation patterns, open work context, running commands, and other session signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad inspection of private session context, including browser state, open files, command or process information, and conversation history.

Mitigation: Constrain the agent to ask for consent before reading sensitive session context and keep access limited to what is needed for the immediate task.

Risk: The skill describes learning from user responses, which could create unwanted persistent memory if implemented without limits.

Mitigation: Keep any learned patterns session-scoped unless the user explicitly approves persistent memory.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown and natural-language agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proactive suggestions and response-style guidance; it does not define a structured API output.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
