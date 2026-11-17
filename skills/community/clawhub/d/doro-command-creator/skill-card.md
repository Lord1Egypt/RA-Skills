## Description:

Creates Claude Code slash commands as reusable markdown workflows invoked with /command-name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a2mus](https://clawhub.ai/user/a2mus)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to create reusable project-local or global Claude Code slash commands for repetitive workflows and consistent processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary identifies an unpinned remote installer as a review concern.

Mitigation: Install only from a pinned, reviewed source when possible.

Risk: Generated persistent slash commands can automate broad workflows such as staging files, committing, pushing, publishing pull requests, or running shell commands.

Mitigation: Review generated command file contents before use and require explicit user confirmation for broad or publishing workflows.

Risk: Global command placement can affect future agent behavior across projects.

Mitigation: Prefer project-local commands unless global behavior is deliberately needed.

## Reference(s):

- [Doro Command Creator on ClawHub](https://clawhub.ai/a2mus/skills/doro-command-creator)
- [Command Best Practices](artifact/references/best-practices.md)
- [Command Patterns](artifact/references/patterns.md)
- [Command Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown command files with YAML frontmatter and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write command files under project-local or global command directories based on user choice and repository context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
