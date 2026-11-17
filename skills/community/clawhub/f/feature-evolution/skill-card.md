## Description:

Feature Evolution guides agents through feature-change analysis, impact assessment, incremental documentation updates, and change-task planning for in-progress or completed features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cping6](https://clawhub.ai/user/cping6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product owners, and technical planners use this skill to handle change requests for existing feature plans. It helps confirm scope, update requirements and technical planning documents incrementally, and produce CR-numbered task plans before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to update planning files under specs/features, so incorrect assumptions could change requirements or task plans in misleading ways.

Mitigation: Review generated document edits and confirm the impact analysis before relying on the updated plans.

Risk: The workflow stops at analysis and planning, so generated task plans may be mistaken for completed implementation work.

Mitigation: Treat outputs as planning artifacts and hand implementation to the appropriate implementation workflow after review.

## Reference(s):

- [ClawHub skill release: Feature Evolution](https://clawhub.ai/cping6/skills/feature-evolution)
- [Feature Evolution change task template](artifact/assets/feature-evolution-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose, change logs, impact-analysis tables, and incremental task plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance and documentation updates, including CR-numbered change records and regression-validation tasks; it does not implement business code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
