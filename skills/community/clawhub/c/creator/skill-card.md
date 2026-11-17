## Description:

Guide for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-wm](https://clawhub.ai/user/warm-wm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create or update agent skills, plan reusable resources, validate skill structure, and package distributable skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled initialization and packaging scripts can write files in local directories selected by the user.

Mitigation: Run the scripts only in controlled workspaces and inspect target paths before creating or packaging a skill.

Risk: Packaging untrusted skill folders could include files that were not intended for release.

Mitigation: Inspect skill folders before packaging, remove symlinks, and validate the package contents before distribution.

Risk: The security scan verdict is suspicious because of local file-scope weaknesses.

Mitigation: Review the skill before installing it, especially when using it on untrusted skill folders or automated inputs.

## Reference(s):

- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill package files when the bundled packaging script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
