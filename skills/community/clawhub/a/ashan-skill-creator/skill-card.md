## Description:

Create, edit, improve, audit, validate, and package OpenClaw AgentSkills using structured authoring guidance and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashanzzz](https://clawhub.ai/user/ashanzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create new OpenClaw AgentSkills, improve or audit existing skill directories, validate required metadata, and package skills for distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or modified skill files can contain incomplete instructions, misleading guidance, or publishing metadata that is not ready for release.

Mitigation: Review generated skill files before publishing and run the included validation workflow before packaging or release.

Risk: Publishing or packaging actions can distribute unintended content if run without user confirmation.

Mitigation: Keep publishing actions user-approved and inspect package contents before distribution.

Risk: Adapted example scripts may introduce third-party dependencies without version constraints.

Mitigation: Pin any third-party dependencies added when adapting the generated examples.

## Reference(s):

- [Workflow Patterns Reference](artifact/references/workflow-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional generated files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill directories, SKILL.md files, optional resource folders, and .skill packages when requested by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
