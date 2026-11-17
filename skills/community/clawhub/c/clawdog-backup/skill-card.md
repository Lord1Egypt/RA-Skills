## Description:

Backs up OpenClaw core files and memory to OneDrive, supports real-time and scheduled backups, and restores from cloud or local backup files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-crazy](https://clawhub.ai/user/michael-crazy)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to preserve and restore agent identity, user, tool, core instruction, and memory state across local environments and OneDrive-backed backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill backs up sensitive OpenClaw identity, user, tool, instruction, and memory state to OneDrive.

Mitigation: Install only when this backup behavior is intended, use a tightly controlled OneDrive and rclone configuration, and prefer client-side encryption.

Risk: Restoring untrusted backups can place unverified files into agent identity, instruction, tool, and memory locations.

Mitigation: Restore only from trusted backups, inspect backup contents before use, and run dry-run restores before writing to a workspace.

Risk: The background monitor can continue uploading changes after the launch command returns.

Mitigation: Start the monitor only with a clear stop procedure and review backup logs during operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michael-crazy/skills/clawdog-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore guidance for OpenClaw files, OneDrive paths, logs, and script options.]

## Skill Version(s):

1.0.1 (source: server release metadata, artifact _meta.json, and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
