## Description:

Framework core engineer skill for CLI commands, code generation standards, PHP 8.4 compatibility, and framework-safe scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or repair Weline CLI commands, scaffold generated code, refresh command registration, and apply framework-specific PHP 8.4 and Windows command-quoting guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or scaffolded command code can introduce incorrect behavior or stale command registration in a Weline repository.

Mitigation: Review the generated code, run the framework command metadata refresh when registration changes, and validate the new or updated command with a focused scenario.

Risk: Shell command composition, especially on Windows-sensitive paths, can fail or behave unexpectedly if quoting is fragile.

Mitigation: Validate shell commands on the intended platform and apply explicit quoting discipline before relying on generated command strings.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets when implementation work is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation notes, platform assumptions, affected services, and command registration steps.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
