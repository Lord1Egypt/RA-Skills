## Description:

CI release engineer skill for environment compatibility, Windows-safe command composition, and automation-stable execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect CI and release commands for cross-environment safety, especially Windows or PowerShell quoting, shell composition, PHP compatibility, and repeatable automation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed command execution in CI or release environments can affect automation stability.

Mitigation: Review proposed commands before execution and keep validation runs focused on the intended automation path.

Risk: Windows, PowerShell, or shell-specific quoting differences can change argument shape across environments.

Mitigation: Validate quoting and interpolation on the relevant target shell and document environment assumptions.

Risk: PHP version or null-safety assumptions can break command code used by release automation.

Mitigation: Check PHP-compatibility-sensitive paths before treating the command path as automation-ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/ci-env-command-safety)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with command examples and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include focused command-run evidence, environment assumptions, and remaining portability risks.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
