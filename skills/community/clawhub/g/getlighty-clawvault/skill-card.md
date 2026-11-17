## Description:

Portable identity vault for OpenClaw that syncs knowledge, packages, and memory across machines using user-selected storage or ClawVault Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlighty](https://clawhub.ai/user/getlighty)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to initialize, sync, migrate, and restore an OpenClaw agent environment across machines while keeping per-machine identity files separate by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill syncs sensitive agent identity, memory, project, package, and skill data.

Mitigation: Review configured storage, synced paths, cloud enrollment, and encryption behavior before using it with confidential data.

Risk: Package restore and setup paths can propose or run privileged or remotely influenced commands.

Mitigation: Require human review of package diffs and generated install commands before execution.

Risk: Security evidence reports under-disclosed encryption and unsafe high-impact paths.

Mitigation: Treat the release as requiring careful review until content encryption, SSH verification, package restore validation, and rclone installation handling are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/getlighty/skills/getlighty-clawvault)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides provider setup, sync, migration, profile, package, and key-management workflows.]

## Skill Version(s):

3.0.0 (source: server release metadata; artifact CLI version agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
