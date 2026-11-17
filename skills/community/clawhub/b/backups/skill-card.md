## Description:

Implement reliable backup strategies avoiding data loss, failed restores, and security gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, system administrators, and operators use this skill to review backup plans for restore testing, retention, ransomware protection, database backup methods, and storage failure domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive backup commands or incorrect source and destination selection can delete source data.

Mitigation: Verify destructive commands such as rsync --delete before running them, prefer dry runs where available, and test restores in a controlled environment.

Risk: Untested backups, missing restore procedures, or lost repository credentials can prevent recovery during an incident.

Mitigation: Schedule restore tests, record recovery time, document recovery steps outside the backup, and store recovery credentials securely.

Risk: Backups reachable from production systems can be encrypted, deleted, or corrupted during ransomware or account-compromise events.

Mitigation: Use air-gapped, offline, append-only, or immutable storage and verify recovery from those protected copies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/backups)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior; operational recommendations should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
