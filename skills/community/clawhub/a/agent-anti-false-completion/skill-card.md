## Description:

Helps agents reduce false completion claims by enforcing task constraints, verification checklists, escalation prompts, and end-to-end delivery habits across coding, debugging, research, writing, planning, operations, API integration, data analysis, and deployment tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[initail](https://clawhub.ai/user/initail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, researchers, and other agent users use this skill to push an agent toward concrete investigation, verification, broader issue checking, and structured handoff instead of unsupported completion claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pressure an agent to broaden investigations and use available tools before asking clarifying questions.

Mitigation: Install only when that aggressive coaching style is desired, and keep host-agent permission prompts enabled for actions outside the user's explicit scope.

Risk: The skill may be inappropriate in production, private, costly, or sensitive environments because it encourages proactive tool use and scope expansion.

Mitigation: Use it only in environments with strict permissions, scoped credentials, and user approval for sensitive or costly operations.

Risk: The security verdict is suspicious because the prompt can alter response format and behavior across many task types.

Mitigation: Review the generated plan and final answer for scope, tone, and requested format compliance before relying on the agent's output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/initail/skills/agent-anti-false-completion)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklists, escalation prompts, and task-handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language agent-coaching content that may direct an agent to use available tools, verify work, broaden investigation, and report risks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
