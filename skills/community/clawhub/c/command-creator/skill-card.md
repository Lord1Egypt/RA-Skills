## Description:

Command Creator helps developers create Claude Code slash commands as reusable Markdown workflows invoked with /command-name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers use this skill to define repeatable Claude Code slash commands, choose a command pattern, gather required inputs, and write command Markdown files for project or global use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands can automate broad repository actions such as editing files, staging all changes, creating commits, publishing pull requests, or running project scripts.

Mitigation: Require explicit confirmation steps in generated commands before destructive, broad, or externally visible actions.

Risk: The README's npx add installation command does not provide an immutable, pinned installation source.

Mitigation: Review the skill before installing and prefer an immutable, pinned source for installation.

Risk: Examples may normalize high-impact workflows without enough safety boundaries.

Mitigation: Review generated slash commands for scoped file targets, clear stopping conditions, error handling, and user approval checkpoints before use.

## Reference(s):

- [Command Creator Skill Page](https://clawhub.ai/wpank/skills/command-creator)
- [Command Patterns](references/patterns.md)
- [Command Best Practices](references/best-practices.md)
- [Command Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with frontmatter and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces slash-command instructions and may create command files under project or global command directories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
