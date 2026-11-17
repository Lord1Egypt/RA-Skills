## Description:

Cleans aborted OpenClaw sub-agent session files and aged backup files while preserving recently updated sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenixmiao](https://clawhub.ai/user/phenixmiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to preview and clean stale aborted sub-agent sessions and backup files, reclaiming disk space while keeping the session index consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad deletion commands in the README can delete unintended session backup files if run directly.

Mitigation: Avoid the raw rm/find commands; require a dry-run or explicit file list in the verified OpenClaw sessions directory before deletion.

Risk: The README references cleanup.sh, but the release artifact does not include that script.

Mitigation: Do not rely on the missing script path; use the documented preview-and-confirm workflow based on session metadata.

Risk: Cleaning session files can remove OpenClaw session history and backups.

Mitigation: Delete only confirmed aborted sub-agent sessions older than 48 hours and preserve recent reset backups according to the documented retention window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phenixmiao/skills/cleanup-sessions)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before deletion and should present a file list before cleanup.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
