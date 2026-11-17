## Description:

Dr Backup Gui is a PyQt6 disaster-recovery GUI that integrates Velero Kubernetes backup and restore, rclone cloud storage sync, rsync file sync, and Coriolis VM migration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhouzhao](https://clawhub.ai/user/chenzhouzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to launch a GUI for backup, restore, storage synchronization, file synchronization, and VM migration tasks across Kubernetes, cloud storage, file systems, and Coriolis-managed clouds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GUI can run backup, restore, sync, mirror, delete, and migration operations that affect live infrastructure or data.

Mitigation: Review the active Kubernetes context and all rclone, rsync, and Coriolis targets before execution; test in non-production first and use dry-run or check modes where available.

Risk: Local profile storage may contain sensitive operational metadata in plaintext.

Mitigation: Restrict permissions on ~/.dr_backup_gui and avoid committing profiles.json, config.json, jobs.json, or activity.log to shared repositories.

Risk: Dependency installation guidance includes package installation and a curl-to-kubectl style Velero install command.

Mitigation: Install in a pinned virtual environment where possible and review any downloaded Kubernetes manifests before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzhouzhao/skills/dr-backup-gui)
- [Publisher profile](https://clawhub.ai/user/chenzhouzhao)
- [rclone installation documentation](https://rclone.org/install/)
- [Coriolis documentation](https://Coriolis.readthedocs.io/)
- [Velero install manifest](https://raw.githubusercontent.com/vmware-tanzu/velero/main/install)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and GUI workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a local PyQt6 GUI that writes profiles, jobs, and logs under ~/.dr_backup_gui.]

## Skill Version(s):

1.0.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
