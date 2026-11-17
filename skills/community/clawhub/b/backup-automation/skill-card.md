## Description:

Automated backup for OpenClaw instances. Backs up agents, skills, cron jobs, and memory. Supports local tar archives. Credentials, periodic scheduling, and git sync are OPT-IN only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzargona](https://clawhub.ai/user/jzargona)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to back up local OpenClaw agents, skills, cron configuration, memory, and core configuration files, then list, inspect status for, or restore those archives when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore extracts an archive into the home directory and can overwrite existing files.

Mitigation: Restore only from trusted, expected backup archives after confirming the selected backup name and taking a fresh backup of current state.

Risk: Git sync can disclose broad OpenClaw workspace data if enabled against an unsuitable remote repository.

Mitigation: Enable git sync only for a dedicated backup repository after reviewing the remote, commit contents, and access controls.

Risk: Backup archives may contain sensitive local configuration, and credentials can be included when the opt-in marker is enabled.

Mitigation: Keep backup archives in a protected location, leave credential backup disabled unless required, and treat produced archives as sensitive data.

Risk: The security guidance flags manually named or untrusted restore archives as unsafe until restore-name validation avoids shell command construction.

Mitigation: Do not restore untrusted or manually renamed archives; validate archive names and paths before invoking restore.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jzargona/skills/backup-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash and JavaScript examples; the script produces local tar.gz backup archives and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credentials backup, periodic scheduling, and git sync are opt-in behaviors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
