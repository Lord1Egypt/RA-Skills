## Description:

Provides git-powered versioned backups and safe snapshot recovery for workspace files, with automated and manual snapshot options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taco-devs](https://clawhub.ai/user/taco-devs)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure ClawKeep snapshots, restore workspace state, and set up encrypted local, S3-compatible, or ClawKeep Cloud backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust the global clawkeep npm CLI.

Mitigation: Pin and verify the CLI version where possible before using it on important workspaces.

Risk: Backup, restore, watch, UI, and sync commands can read, snapshot, restore, and sync broad workspace contents.

Mitigation: Review ignore patterns, test restores in a separate directory first, and stop watch, UI, or PM2 daemons when they are no longer needed.

Risk: Cloud and S3 workflows require credentials or API keys that could expose backup destinations if mishandled.

Mitigation: Use least-privilege S3 or API keys and avoid placing real secrets directly on command lines.

## Reference(s):

- [ClawKeep Skill Page](https://clawhub.ai/taco-devs/skills/clawkeep)
- [Primary ClawKeep Skill Documentation](artifact/SKILL.md)
- [Local Backup Target Documentation](artifact/local/SKILL.md)
- [S3 and R2 Backup Target Documentation](artifact/s3/SKILL.md)
- [ClawKeep Cloud Target Documentation](artifact/clawkeep-cloud/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, status, restore, sync, daemon, and troubleshooting guidance for workspace backup workflows.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
