## Description:

Auto-update OpenClaw and skills with OpenClaw cron, per-skill defaults, backups, and migration-aware summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure a scheduled maintenance flow that checks OpenClaw and installed ClawHub skills, applies approved updates, creates backups, pauses on migration risk, and summarizes results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent auto-update workflow can apply changes on a schedule the user did not intend.

Mitigation: Confirm the exact scheduler entry and choose auto, notify, or manual mode for OpenClaw before enabling recurring runs.

Risk: Skill updates can introduce migration changes to paths, state files, or workspace hooks.

Mitigation: Pause updates with pending or ask-first migration states, show the user what changed, and ask before moving or deleting anything.

Risk: Backups may include sensitive OpenClaw credential material if the backup scope is too broad.

Mitigation: Avoid backing up ~/.openclaw/credentials/ unless the user has a secure encrypted destination and a clear recovery need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/auto-update)
- [Skill homepage](https://clawic.com/skills/auto-update)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration ledger templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local policy files, scheduler commands, backup and migration records, run logs, and update summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
