## Description:

CI release engineer skill for environment compatibility, Windows-safe command composition, and automation-stable execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to make CI automation, shell commands, PowerShell paths, and PHP-sensitive command code more portable and repeatable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to propose command changes or focused validation commands for CI and release automation.

Mitigation: Review proposed command changes and validation commands before use, especially on Windows, PowerShell, PHP, or release paths.

Risk: Cross-environment command behavior may remain unverified when the target shell or CI runner is unavailable.

Mitigation: Document environment assumptions and run the narrowest confirming command on the intended shell path before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/ci)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with command examples and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment assumptions and remaining portability risks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
