## Description:

Manage Apple Notes via the `memo` CLI on macOS to create, view, edit, delete, search, move, and export notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to manage Apple Notes from a macOS terminal through the memo CLI, including note creation, search, folder moves, deletion, and local export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI that may receive access to private Apple Notes.

Mitigation: Install only if the memo project and Homebrew tap are trusted, and prefer a pinned, verified release or reviewed commit before granting Notes.app Automation access.

Risk: Delete and move operations can remove or reorganize private notes.

Mitigation: Confirm note names and destinations one at a time before destructive or bulk changes.

Risk: Exported note contents could expose private data if sent to network tools.

Mitigation: Keep note exports local and do not pipe or redirect note contents to curl, wget, ssh, nc, APIs, or similar network-transmitting commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/apple-notes-hardened)
- [memo CLI project](https://github.com/antoniorodr/memo)
- [Faberlens Apple Notes safety evaluation](https://faberlens.ai/explore/apple-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires Apple Notes.app, Automation permissions, and the memo CLI.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
