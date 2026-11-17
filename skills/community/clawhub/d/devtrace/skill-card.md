## Description:

DevTrace provides a Chinese framework for evaluating technical and architecture decisions through topology, abstraction, entropy, constraints, and dependency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kings0527](https://clawhub.ai/user/kings0527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and technical reviewers use this skill to structure architecture decisions, technology selection, code review, refactoring evaluation, technical debt assessment, and project risk analysis. It helps agents produce dependency topology, maintainability, constraint, risk, and recommendation outputs for engineering decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can impose a structured Chinese topology, entropy, dependency, and recommendation format whenever a technical decision is discussed.

Mitigation: Use it when that decision framework is desired, and explicitly specify another language or output shape when a lighter or different format is needed.

Risk: Decision guidance can be incomplete when architecture, dependency, operational, or constraint context is missing.

Mitigation: Require the agent to ask focused clarifying questions or state conditional conclusions with explicit assumptions before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kings0527/skills/devtrace)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown guidance in Chinese with topology, entropy, dependency, conclusion, and follow-up sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask clarifying questions when decision context is insufficient; does not execute tools or access data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
