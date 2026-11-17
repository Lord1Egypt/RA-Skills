## Description:

Guide for creating effective skills that extend an agent with specialized knowledge, workflows, and tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixinda](https://clawhub.ai/user/jixinda)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to design, implement, validate, and package agent skills with clear triggering metadata, concise instructions, and reusable resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging workflow can accidentally include files outside the intended skill directory through symlinks.

Mitigation: Inspect skill directories for symlinks before packaging and package only reviewed, trusted directories.

Risk: Untrusted skill names or output paths passed to initialization tooling can create unexpected filesystem changes.

Mitigation: Use trusted, validated skill names and explicit output directories when initializing new skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jixinda/skills/flyai-test)
- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and generated skill files or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update skill package files, validation output, and packaging commands depending on the user request.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
