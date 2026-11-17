## Description:

Exports a user's ChatGPT conversation history to local JSON and Markdown files, defaulting to index-only metadata unless full message text is explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create local backups or readable archives of their own ChatGPT conversation history. It supports index-only exports for titles and timestamps, with full message text only when explicitly requested and confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports can create plaintext local copies of sensitive ChatGPT conversation data.

Mitigation: Prefer index-only mode unless message text is needed, keep exports out of synced folders, and delete completed exports with the documented purge command.

Risk: The skill uses the logged-in ChatGPT browser session to access the user's own conversation history.

Mitigation: Install only if that access pattern is acceptable, require explicit confirmation before export, and use the documented off switch when exports should be disabled.

Risk: Cleanup commands delete local export directories when explicitly invoked.

Mitigation: Use the validated purge path only for directories created by the tool; it requires a manifest, canonical path checks, and interactive confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/chatgpt-exporter)
- [Publisher profile](https://clawhub.ai/user/globalcaos)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Local JSON and Markdown files with console guidance for confirmation, destination checks, and cleanup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default relay export is index-only; full message text is optional, local, and written to private file modes when the relay path is used.]

## Skill Version(s):

1.9.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
