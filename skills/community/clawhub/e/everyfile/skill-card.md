## Description:

everyfile helps agents find, list, and count files or folders on Windows using Voidtools Everything through the ev CLI or Python API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisgamedev](https://clawhub.ai/user/louisgamedev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform fast Windows file discovery, counts, duplicate checks, and result processing when Voidtools Everything is installed and running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filesystem searches can reveal sensitive file paths or locate sensitive files such as .env files.

Mitigation: Scope queries where possible, review matches before sharing or processing them, and avoid exposing sensitive paths or file contents.

Risk: Examples that pipe search results into shell commands can move, modify, or otherwise affect many files if used carelessly.

Mitigation: Use counts and result limits before bulk operations, inspect candidate paths, and confirm with the user before running destructive or large-scale commands.

Risk: The skill depends on a Windows-only search stack and a local everyfile package installation.

Mitigation: Install only reviewed or pinned package versions and use the skill only when Windows, Voidtools Everything, and the ev binary are available.

## Reference(s):

- [everyfile ClawHub skill page](https://clawhub.ai/louisgamedev/skills/everyfile)
- [Voidtools Everything](https://www.voidtools.com/)
- [CLI Reference](references/cli.md)
- [Python API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs commonly include file paths, counts, NDJSON examples, and API usage patterns.]

## Skill Version(s):

2026.4.22 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
