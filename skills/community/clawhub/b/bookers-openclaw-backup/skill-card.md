## Description:

Create, inspect, configure, and restore self-contained backup bundles for ~/.openclaw. Use when the user wants full-state backup, backup listing, changing the default backup directory, bundle selection, or guarded restore of OpenClaw state. Public default path is ~/backups/openclaw-snapshots; private local setups can override it with config or CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silronin](https://clawhub.ai/user/silronin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create portable backups of ~/.openclaw, inspect saved bundles, configure snapshot storage, and perform guarded restores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup bundles may expose sensitive OpenClaw state if stored with loose local permissions.

Mitigation: Store backup bundles in a private directory, restrict local access, and avoid shared or untrusted storage.

Risk: The restore flow can direct users to run restore.sh from a backup bundle.

Mitigation: Restore only bundles the user created and trusts, and avoid running restore.sh from bundles received through shared or untrusted storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silronin/skills/bookers-openclaw-backup)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and local configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for creating, listing, configuring, selecting, auditing, and restoring OpenClaw backup bundles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
