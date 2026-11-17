## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceundefeated](https://clawhub.ai/user/aceundefeated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking users use this skill to let an agent locate active Obsidian vaults, inspect Markdown notes, and propose or run obsidian-cli commands for search, creation, move, rename, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent read, create, move, and delete notes in an Obsidian vault.

Mitigation: Confirm vault paths and target note paths before move or delete operations, and rely on backups or version history for important notes.

Risk: The skill depends on a third-party obsidian-cli Homebrew tap.

Mitigation: Install obsidian-cli only after deciding the Homebrew tap and package source are trusted.

Risk: Some create workflows require the Obsidian URI handler and an installed Obsidian desktop app.

Mitigation: Verify Obsidian is installed and the obsidian:// URI handler works before using create commands that open notes through Obsidian.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [Aj Obsidian on ClawHub](https://clawhub.ai/aceundefeated/skills/aj-obsidian)
- [aceundefeated ClawHub profile](https://clawhub.ai/user/aceundefeated)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, vault names, and obsidian-cli command examples for local note operations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
