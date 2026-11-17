## Description:

Back up OpenClaw customizations (memory, config, skills, workspace) to cloud storage via rclone, with scheduling + retention. Works on macOS, Linux, and Windows (Git Bash/WSL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vidarbrekke](https://clawhub.ai/user/vidarbrekke)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to generate and schedule backups of local OpenClaw configuration, memory, skills, workspace files, and related project data to a local or rclone-backed destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick install path can execute changing remote code before review.

Mitigation: Clone and pin the repository first, then inspect setup.js and install-launchagent.sh before running setup.

Risk: Scheduler setup may run unintended commands under the user account.

Mitigation: Avoid enabling the scheduler until the Bash escaping issue is fixed, and inspect generated LaunchAgent, cron, or Task Scheduler entries before use.

Risk: Backups may contain sensitive OpenClaw configuration, memory, workspace, and skill data.

Mitigation: Use local-only mode for testing and prefer encrypted rclone destinations or local archive encryption before offsite storage.

Risk: The macOS installer can remove a system LaunchDaemon with sudo.

Mitigation: Do not approve sudo removal unless you intentionally want that exact system service removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vidarbrekke/skills/claw-backup)
- [rclone installation documentation](https://rclone.org/install/)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline bash and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate backup scripts, scheduler setup instructions, restore notes, manifests, and checksum files when run by the user.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; artifact SKILL.md reports 1.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
