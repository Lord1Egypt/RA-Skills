## Description:

Lint your Claude Code config for token waste. Checks CLAUDE.md, hooks, skills, and commands. Gives health score and actionable fixes. Use when user asks about config optimization or token waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singggggyee](https://clawhub.ai/user/singggggyee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to inspect local Claude Code configuration for token waste and receive health scoring with actionable fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the separate cclint CLI, whose implementation is not included in the skill artifact.

Mitigation: Review the cclint package before installation and execution.

Risk: The linter reads local Claude Code configuration files, including CLAUDE.md, settings.json, skills, and commands.

Mitigation: Install and run it only when local configuration inspection is acceptable.

## Reference(s):

- [cclint CLI repository](https://github.com/SingggggYee/cclint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from cclint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the cclint CLI, which reads local Claude Code configuration files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
