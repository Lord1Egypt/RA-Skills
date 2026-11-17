## Description:

Disk Cleaner helps agents scan Windows, macOS, and Linux systems for cache and temporary-file cleanup candidates, classify them by deletion safety, and guide user-confirmed cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and workstation users use this skill when disk space is low or they need to inspect and clean package-manager, IDE, application, log, temporary, and discovered cache directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended data loss from deleting cache-like directories or temporary files.

Mitigation: Run --dry-run first, inspect the generated deletion list and full paths, select only intended items, avoid --force, and do not run as administrator or root.

Risk: Discovered items, Electron application storage, IDE local history, logs, or symlinked cache directories may contain data the user expects to keep.

Mitigation: Treat discovered items as review-only candidates, use --no-discover for conservative scans, verify each selected path, and skip entries whose contents or ownership are unclear.

Risk: Cleaning the recycle bin or trash can make recovery harder after a mistaken selection.

Mitigation: Use --no-trash when validating a cleanup plan or when recoverability is more important than immediately reclaiming all space.

## Reference(s):

- [Cleanup Catalog](references/cleanup-catalog.md)
- [Platform Paths](references/platform-paths.md)
- [ClawHub Skill Page](https://clawhub.ai/liyumingben/skills/disk-cleaner)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; JSON when the cleanup script is run with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run reports and selected cleanup plans before deletion.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
