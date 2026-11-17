## Description:

Comprehensive backup, update, and restore workflow with dynamic workspace detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to prepare for Clawdbot updates by checking upstream changes, validating setup, creating backups, following update steps, and restoring from backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain credentials, tokens, sessions, workspaces, cron state, and configuration.

Mitigation: Store generated backups as secret material and avoid placing them in shared or synced locations.

Risk: Restoring an untrusted or stale backup can overwrite current Clawdbot configuration and state.

Mitigation: Verify the backup source, inspect archive contents, and make a fresh current backup before restoring.

Risk: The security verdict requires review before installation.

Mitigation: Install only when the publisher is trusted and the skill will be used with trusted backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pasogott/skills/clawdbot-skill-update)
- [Publisher Profile](https://clawhub.ai/user/pasogott)
- [Clawdbot Project Repository](https://github.com/clawdbot/clawdbot)
- [Skill Homepage](https://github.com/pasogott/clawdbot-skill-update)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, jq, tar, and git according to ClawHub metadata.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
