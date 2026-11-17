## Description:

Search files and folders on Windows using Everything CLI with advanced filters, wildcards, regex, macros, sorting, and real-time indexing features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dahanhstudio](https://clawhub.ai/user/dahanhstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and Windows power users use this skill to install and operate Everything's es.exe command line search, compose advanced file queries, and use helper scripts for repeated searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Everything indexes local filesystem paths and metadata, which may expose sensitive filenames or locations to users or tools that can query it.

Mitigation: Install only where local filesystem indexing is acceptable, and restrict use to trusted accounts and intended search scopes.

Risk: The Bash wrapper is flagged by server security guidance because it uses eval when executing constructed commands.

Mitigation: Avoid the Bash wrapper until eval is removed; prefer direct es.exe usage or review and harden the wrapper before execution.

Risk: The artifact includes remote HTTP and ETP server guidance that can expose search or file access over a network.

Mitigation: Enable HTTP or ETP servers only on trusted networks, with strong credentials and a documented need for remote access.

Risk: The examples include a forced-delete PowerShell cleanup pattern.

Mitigation: Do not copy the forced-delete example into automation without a dry run, explicit path constraints, and manual review of matched files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dahanhstudio/skills/everything-cli-search)
- [Everything documentation](https://www.voidtools.com/support/everything/)
- [Everything download](https://www.voidtools.com/)
- [Everything command line options](https://www.voidtools.com/support/everything/command_line_options)
- [Everything HTTP server](https://www.voidtools.com/support/everything/http)
- [Everything ETP server](https://www.voidtools.com/support/everything/etp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused; requires Everything and es.exe to be installed and available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
