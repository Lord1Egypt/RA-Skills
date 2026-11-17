## Description:

Distill Skill Builder guides agents through turning official documentation into structured knowledge skills, including source analysis, content collection or distillation, skill organization, evaluation, and quality iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, evaluate, improve, and package knowledge-focused agent skills from documentation sources. It is intended for workflows that need repeatable skill structure, reference material, scoring, and iteration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to fetch content from remote documentation sources.

Mitigation: Approve each URL before crawling, avoid untrusted or internal URLs, and perform collection in a staging workspace.

Risk: Generated skills or copied files could introduce prompt-injection content into active assistant directories.

Mitigation: Review and scan generated skill files before deployment, and only copy them into active assistant paths after approval.

Risk: Evaluator patch suggestions could alter quality gates outside normal maintenance controls.

Mitigation: Apply evaluator changes only when the evaluator is maintained under normal code review and test coverage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yhongm/skills/distill-skill-builder)
- [README](artifact/README.md)
- [Skill Distillation Workflow](artifact/references/distillation-workflow.md)
- [Data Crawling Methodology](artifact/references/crawling-guide.md)
- [Skill Evaluator Guide](artifact/references/evaluator-guide.md)
- [Skill Metadata Field Specification](artifact/references/metadata-spec.md)
- [SKILL.md Structure Specification](artifact/references/skillmd-structure.md)
- [Skill Naming and Classification](artifact/references/naming-conventions.md)
- [Skill Quality Standards](artifact/references/quality-standards.md)
- [Skill Iteration Playbook](artifact/references/iteration-guide.md)
- [Skill Quality Checklist](artifact/references/self-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, checklists, and file-structure recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose crawling steps, generated skill files, evaluator runs, and deployment copy steps that require user review before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
