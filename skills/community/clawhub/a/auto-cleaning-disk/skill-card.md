## Description:

Automatically clean disk space by removing temp files, browser cache, recycle bin or trash, and log files on Windows, Linux, and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to free disk space by running operating-system-specific cleanup guidance or scripts for temporary files, browser caches, trash, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete local files from broad cache, temp, log, browser-profile, trash, and Windows update-cache locations.

Mitigation: Review targets before installing or running; avoid Auto Mode and administrator or root privileges unless paths are narrowed, file-age checks are enforced, and a dry-run preview with explicit confirmation is added.

Risk: The skill's safety promises understate how much local data may be deleted.

Mitigation: Use Confirm Mode, review each cleanup category, and skip any path or file set whose contents are unclear.

## Reference(s):

- [Auto Cleaning Disk on ClawHub](https://clawhub.ai/ahqazi-dev/skills/auto-cleaning-disk)
- [Windows Disk Cleaner](artifact/windows-cleaner.md)
- [Linux Disk Cleaner](artifact/linux-cleaner.md)
- [macOS Disk Cleaner](artifact/mac-cleaner.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with Python cleanup commands or scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cleanup summaries showing space freed, categories cleaned, and skipped items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
