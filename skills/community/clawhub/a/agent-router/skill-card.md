## Description:

Routes user commands to the most suitable sub-agent based on intent, coordinates execution priority when multiple skills trigger, and tracks task status for a consolidated response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zs15600770520](https://clawhub.ai/user/zs15600770520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route user requests to appropriate sub-agents or skills, coordinate priority when multiple skills match, and summarize subtask status into one response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected routing prompts are Chinese-language focused and may not fit multilingual routing workflows.

Mitigation: Add equivalent triggers or fallback language guidance before using it in multilingual agent setups.

Risk: Intent routing and priority coordination can send work to the wrong sub-agent if local priorities do not match the user's workflow.

Mitigation: Review the routing triggers and priority behavior against the intended agent set before deployment.

## Reference(s):

- [Agent Router on ClawHub](https://clawhub.ai/zs15600770520/skills/agent-router)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown or plain text routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential access, or hidden behavior was identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
