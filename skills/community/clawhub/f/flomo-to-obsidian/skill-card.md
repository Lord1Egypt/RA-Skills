## Description:

Parses and syncs Flomo exported HTML data into an Obsidian vault, with support for manual conversion, automatic sync, attachments, tags, and incremental updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perseveringman](https://clawhub.ai/user/perseveringman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and note-taking users use this skill to import Flomo notes into Obsidian, convert exports to Markdown, and set up recurring synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password-based automation may expose Flomo credentials through chat, local configuration, or shell environment handling.

Mitigation: Prefer browser-session safe mode, avoid pasting passwords into chat, and avoid password mode until credential storage and environment-file handling are hardened.

Risk: Local file conversion and attachment handling may process untrusted exports or write unexpected files into a vault.

Mitigation: Convert only trusted Flomo exports, review the destination vault path before execution, and be especially cautious when the vault syncs to cloud storage.

Risk: Recurring sync setup can continue running after the user no longer expects it.

Mitigation: Document the scheduled task location, retain removal instructions with the user, and review cron or scheduler entries after setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perseveringman/skills/flomo-to-obsidian)
- [Flomo web app](https://flomoapp.com)
- [Artifact README](artifact/README.md)
- [Safe mode usage guide](artifact/USAGE_SAFE_MODE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated Obsidian Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Obsidian Markdown files, attachment copies, sync state, browser session data, logs, and scheduled sync configuration when the user authorizes those workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
