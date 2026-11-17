## Description:

Evaluates whether a described workflow is suitable for an AI agent and provides agent design recommendations based on established best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaxinmmhh](https://clawhub.ai/user/jiaxinmmhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and workflow owners use this skill to decide whether a workflow should be implemented with an AI agent. When a workflow appears suitable, the skill provides concise guidance on model capability needs, tool design, instructions, orchestration, and guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent suitability and design recommendations may be over-applied without a full architecture review.

Mitigation: Treat the output as advisory, validate it with the responsible technical team, and use real user feedback before expanding the agent design.

Risk: The skill is written for Chinese-language guidance and may not match a user's language preference in other contexts.

Mitigation: Clarify the desired response language before applying the guidance in non-Chinese conversations.

## Reference(s):

- [Agent 构建评估决策框架](references/evaluation-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown advisory assessment with structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; does not provide code implementations or specific model names.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
