## Description:

Feature Task Planning converts approved feature requirements and technical designs into executable, TDD-ready development task plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cping6](https://clawhub.ai/user/cping6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill after requirements and technical design are approved to break a feature into vertical slices, ordered implementation tasks, dependencies, effort estimates, and TDD-ready verification criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a Markdown task plan under specs/features, which could replace or conflict with an existing plan.

Mitigation: Review the destination path and existing files before allowing generation.

Risk: Task plans can be misleading if the referenced requirements, technical design, or project context are missing or stale.

Mitigation: Confirm the stated prerequisites and cross-check AC coverage before using the plan for implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cping6/skills/feature-task-planning)
- [Feature task planning template](artifact/assets/feature-task-planning-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown task plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a feature task plan under specs/features after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
