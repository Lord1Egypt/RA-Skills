## Description:

Agent Architect diagnoses whether an agent issue belongs in persona, rules, memory, or skills, then recommends the smallest justified fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent maintainers, and operators use this skill to diagnose recurring agent behavior problems and decide whether the smallest appropriate change belongs in persona, rules, memory, or a reusable skill workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause agents to record architecture recommendations in memory, which may preserve incorrect or premature diagnoses.

Mitigation: Review the diagnosis and require explicit operator approval before writing durable memory or applying structural recommendations.

Risk: The artifact includes a hard-coded named approval authority in its placement guidance.

Mitigation: Replace that approval rule with the installing team's authenticated governance policy before relying on it.

## Reference(s):

- [Lane Diagnosis](references/lane-diagnosis.md)
- [Fix Types](references/fix-types.md)
- [Audit Checklist](references/audit-checklist.md)
- [Placement Map](references/placement-map.md)
- [Worked Examples](references/worked-examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with optional YAML structured output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic recommendations may include patch targets and risks to avoid; proposals require review before changes are applied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
