## Description:

Back up and restore your OpenClaw workspace, including memory, skills, and configuration, using local or cloud backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chelouche9](https://clawhub.ai/user/chelouche9)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to discover, back up, restore, encrypt, schedule, and optionally sync workspace data across machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to run unpinned npm code for backup, restore, cloud sync, and scheduled jobs that handle sensitive workspace data.

Mitigation: Review the Clawon package, prefer a locally audited install, and pin a trusted version before executing commands.

Risk: Scheduled backups create persistent crontab entries and may repeatedly process workspace data.

Mitigation: Inspect the generated crontab entry and disable or edit the schedule when it is no longer needed.

Risk: Including sessions, memory databases, or credentials can expose sensitive data, especially during cloud backup.

Mitigation: Run discovery first, keep secrets excluded unless necessary, require encryption for cloud secrets, and store encryption passphrases securely.

## Reference(s):

- [Clawon Skill Listing](https://clawhub.ai/chelouche9/skills/clawon)
- [Clawon Homepage](https://clawon.io)
- [Clawon npm Package](https://www.npmjs.com/package/clawon)
- [Clawon Source Repository](https://github.com/chelouche9/clawon-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may perform local backup, restore, cloud sync, scheduling, encryption, and discovery actions through the Clawon CLI.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
