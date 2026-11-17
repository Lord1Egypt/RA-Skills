## Description:

Clawdbot Filesystem.Bak provides advanced filesystem operations for listing, searching, batch processing, copying, and directory analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choichuncj](https://clawhub.ai/user/choichuncj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect directories, search filenames or file contents, copy matched files, render directory trees, and summarize filesystem structure within an allowed workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad filesystem access and can guide read, search, copy, and analysis operations over local directories.

Mitigation: Install it only in a constrained workspace, grant the smallest necessary directory scope, and prefer read-only access where write or copy behavior is not required.

Risk: The server security summary says the declared executable is missing.

Mitigation: Confirm the executable exists and inspect its behavior before enabling the skill for agent use.

Risk: The server security summary says some setup paths would run unpinned external tools.

Mitigation: Pin external tool versions and review installation commands before running them.

Risk: The artifact includes filesystem and PDF-related subskills that may create or modify local files.

Mitigation: Review proposed file changes and generated PDFs before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/choichuncj/skills/clawdbot-filesystem-bak)
- [ClawHub publisher profile](https://clawhub.ai/user/choichuncj)
- [Clawdbot filesystem repository](https://github.com/gtrusler/clawdbot-filesystem)
- [Model Context Protocol filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [Model Context Protocol security best practices](https://modelcontextprotocol.io/docs/concepts/security)
- [nano-pdf package](https://pypi.org/project/nano-pdf/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and filesystem operation outputs such as tables, lists, trees, and JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js according to server-resolved ClawHub metadata; filesystem access should be limited to intended workspaces.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
