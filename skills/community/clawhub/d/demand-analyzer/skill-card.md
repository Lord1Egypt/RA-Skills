## Description:

A seven-part demand analysis framework that prompts an agent to clarify user intent, constraints, missing information, options, and execution plans before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcz-user](https://clawhub.ai/user/zcz-user)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to slow down task intake, identify ambiguity, surface missing information, and present concise options before execution. It is most useful for complex, vague, or underspecified requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation can make the agent pause for structured analysis even when the user expects a concise answer.

Mitigation: Narrow activation to complex or ambiguous tasks, or let users explicitly request the framework.

Risk: Chinese-only templates may not match every user's preferred language.

Mitigation: Mirror the user's language when presenting the framework and adapt labels where needed.

## Reference(s):

- [7 部分需求拆解框架](references/framework.md)
- [ClawHub Skill Page](https://clawhub.ai/zcz-user/skills/demand-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured analysis template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a seven-part requirement analysis with clarification questions, selectable options, and an execution plan.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
