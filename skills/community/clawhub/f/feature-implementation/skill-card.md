## Description:

Guides an agent through TDD-driven feature implementation from existing requirements, technical plans, and task-planning documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cping6](https://clawhub.ai/user/cping6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement planned feature stages with a strict RED-GREEN-REFACTOR loop, then validate acceptance criteria in the appropriate real environment before marking work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to edit code, run tests, update planning files, and create development reports, so incorrect specs or task plans can lead to incorrect implementation work.

Mitigation: Review the referenced requirements, technical plan, and task-planning documents before invoking the skill, and require the stated TDD and acceptance checks before marking work complete.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cping6/skills/feature-implementation)
- [Stage completion report template](assets/stage-completion-report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with code, shell commands, file edits, and generated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update project source files, tests, planning documents, and stage-completion reports as part of the requested implementation task.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
