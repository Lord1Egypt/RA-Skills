## Description:

Routes user requests to specialist agents using rule-based intent matching, task dispatch, result integration, retry handling, fallback behavior, and limited parallel execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate requests across specialist agents for coding, research, writing, design, management, and general fallback tasks. It is most useful when a main agent needs consistent routing rules, retry behavior, and concise result integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically route broad user requests and raw prompt content to other agents.

Mitigation: Avoid sending secrets or sensitive personal or business data unless that content is approved for downstream agent handling.

Risk: Routing metadata logging may expose sensitive task details in operational records.

Mitigation: Review and tighten logging policy before using the skill in sensitive environments.

Risk: Rule-based routing may send requests to an unintended specialist agent or trigger fallback handling.

Mitigation: Review routing patterns and priorities before deployment, and test representative requests for each configured route.

## Reference(s):

- [Daxiang Agent Dispatch on ClawHub](https://clawhub.ai/daxiangnaoyang/skills/daxiang-agent-dispatch)
- [daxiangnaoyang publisher profile](https://clawhub.ai/user/daxiangnaoyang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with agent routing results, examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected agent name, execution timing, retry count, fallback status, and integrated specialist-agent output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
