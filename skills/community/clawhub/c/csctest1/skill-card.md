## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill or update an existing skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenscgit](https://clawhub.ai/user/chenscgit)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to plan, create, validate, package, and iterate on agent skills with focused instructions, supporting scripts, and reference materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags file-safety concerns in the bundled initialization and packaging scripts.

Mitigation: Use the skill only on trusted skill folders, pass explicit output directories, and review generated files before packaging or sharing.

Risk: Packaging untrusted directories may include unsafe or unintended files.

Mitigation: Avoid packaging directories from other people unless symlinks and archive contents have been checked first.

## Reference(s):

- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local skill directories, validation output, and .skill archive packages when its bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
