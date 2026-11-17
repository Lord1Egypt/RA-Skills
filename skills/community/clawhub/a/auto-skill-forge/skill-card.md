## Description:

Skill Forge generates task suites for existing agent skills and can generate a complete SKILL.md plus task_suite.yaml from a structured skill_spec.yaml.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use Skill Forge to create runnable task_suite.yaml coverage for existing skills, generate new skills from a structured YAML spec, and optionally run downstream evaluation or improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SKILL.md files may turn untrusted or poorly reviewed specs into agent instructions.

Mitigation: Review generated SKILL.md files before installation, especially when the spec comes from another person or includes critical constraints.

Risk: The release claims calibration and atomic-write safeguards that the implementation may not fully provide.

Mitigation: Use private output directories, inspect generated files before deployment, and do not rely on documented safeguards until the implementation is verified.

Risk: --auto-improve can invoke another local tool that mutates skill instructions.

Mitigation: Use --auto-improve only in controlled workspaces and review any modified skill instructions before publishing or installing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/auto-skill-forge)
- [Skill Spec Format](references/spec-format.md)
- [Code Review Spec Example](references/examples/code-review-spec.yaml)
- [Release Notes Spec Example](references/examples/release-notes-spec.yaml)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown and YAML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates task_suite.yaml for existing skills, or SKILL.md plus task_suite.yaml from a skill_spec.yaml.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
