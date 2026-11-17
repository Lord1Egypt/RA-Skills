## Description:

Cron-edit-safe wraps OpenClaw cron edits with backup, dry-run, verification, and rollback steps to reduce silent cron breakage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who maintain OpenClaw scheduled jobs use this skill to make cron edits with a backup-first workflow, a pre-edit command check, post-edit verification, and recovery guidance when an edit fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety checks and rollback are reported as unreliable around persistent cron changes.

Mitigation: Review the skill before installing it for important cron jobs, test it on non-critical entries first, keep independent backups, and manually verify cron state after edits.

Risk: Dry-run is real local command execution and can have side effects or expose sensitive environment variables.

Mitigation: Run dry-run commands only in a controlled environment, review command behavior first, and avoid passing sensitive environment variables.

Risk: The advertised rollback should not be treated as a complete restoration mechanism until the identified temp-file handling, verification, and rollback issues are fixed.

Mitigation: Retain the backup JSON and manual recovery command path, and confirm restoration with OpenClaw after any failed edit.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/cron-edit-safe)
- [ClawHub publisher profile](https://clawhub.ai/user/colbertlee)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [CLI text output with OpenClaw cron edits and JSON backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, jq, and OpenClaw CLI; Python is optional for verification parsing.]

## Skill Version(s):

1.0.0 (source: skill.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
