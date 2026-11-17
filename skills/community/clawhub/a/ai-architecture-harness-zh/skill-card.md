## Description:

建立和使用 AI 编程架构护栏，防止架构坍缩、功能回退和长对话迭代漂移。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this Chinese-language skill to create, maintain, and apply architecture guardrails before modifying large or complex codebases. It guides documentation, acceptance checks, architecture drift review, and golden-rule feedback loops to reduce architecture collapse, regression, and long-conversation drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to create or update repository documentation, tests, lint rules, or configuration.

Mitigation: Review proposed repository changes like normal code changes before accepting them.

Risk: Architecture guidance can become inaccurate if it treats current implementation drift as intended design.

Mitigation: Compare updates against human-maintained design intent and keep uncertain differences in architecture drift documentation for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/ai-architecture-harness-zh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional repository documentation, tests, lint rules, shell commands, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language architecture guardrail guidance; repository changes should be reviewed like normal code changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
