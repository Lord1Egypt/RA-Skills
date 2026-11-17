## Description:

Guides agents to check, create, or adjust a standardized project directory structure that separates project files, logs, temporary files, configuration, data, scripts, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when creating a new project, checking whether an existing project follows the expected layout, or reorganizing project files into conventional directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The create script can overwrite placeholder files in an existing path and may follow symlinks outside the selected project directory.

Mitigation: Use the create script only in a new empty directory, or inspect existing files and symlinks before accepting the prompt to continue.

## Reference(s):

- [Quick Start](QUICK_START.md)
- [Project Structure Reference](references/PROJECT_STRUCTURE.md)
- [Gitignore Template](references/GITIGNORE.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and directory structure examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create directories and placeholder files when the bundled create script is run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
