## Description:

Command-line tool to create, read, search, manage, and export local Obsidian notes with JSON output support for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and run a CLI for creating, searching, listing, and managing Obsidian notes in local vaults. It is suited to automating meeting notes, bulk note management, quick search, and data export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and rely on the cli-obsidian package source.

Mitigation: Install only from a trusted package source, preferably in a virtual environment and without administrator privileges.

Risk: The CLI operates on local Obsidian vault content that may include private notes.

Mitigation: Point the CLI only at vaults intended for agent access and avoid exposing sensitive notes to untrusted workflows.

Risk: Automated note management or export can modify or disclose vault data.

Mitigation: Keep backups and review automated create, manage, or export operations before using them on important vaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/cli-obsidian)
- [Publisher profile](https://clawhub.ai/user/kaising-openclaw1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI can return JSON for agent integration; the skill itself provides operational guidance for local note workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/_meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
