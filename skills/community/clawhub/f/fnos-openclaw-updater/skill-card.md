## Description:

Guides agents through checking and updating OpenClaw on fnOS by comparing the running version with the latest npm package and installing the update in the managed-install directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaltsgo](https://clawhub.ai/user/pandaltsgo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw administrators use this skill to update an fnOS OpenClaw gateway without writing to global npm or system application paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite the active OpenClaw gateway from a mutable npm package.

Mitigation: Confirm the target OpenClaw version and package source before running the install.

Risk: The update workflow does not include rollback or staging steps.

Mitigation: Back up or stage the managed install before updating an important gateway.

Risk: Changing npm registry settings can affect later npm commands.

Mitigation: Avoid changing the global npm registry unless that persistent setting is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended to be reviewed before executing npm install against an active OpenClaw gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
