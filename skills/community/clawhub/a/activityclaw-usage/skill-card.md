## Description:

ActivityClaw Plugin Usage helps agents guide users through checking ActivityClaw activity status, opening its dashboard, and reviewing tracked agent activity such as file operations, commands, web actions, messages, and sub-agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmruss2022](https://clawhub.ai/user/rmruss2022)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect recent agent activity, troubleshoot ActivityClaw status, and open the local dashboard for file, command, web, message, and sub-agent history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party ActivityClaw package.

Mitigation: Review the package source and pin a known package version before installation.

Risk: ActivityClaw records broad local agent activity, including files, commands, web actions, messages, and sub-agent history.

Mitigation: Use it only when local activity storage is acceptable, and confirm the database location and deletion process before collecting activity.

Risk: The local dashboard exposes recorded activity on a configurable local service.

Mitigation: Confirm dashboard access restrictions and port configuration before running the service.

## Reference(s):

- [ActivityClaw Plugin Usage on ClawHub](https://clawhub.ai/rmruss2022/skills/activityclaw-usage)
- [ActivityClaw GitHub repository](https://github.com/rmruss2022/ActivityClaw)
- [ActivityClaw npm package](https://www.npmjs.com/package/@rmruss2022/activityclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume the third-party ActivityClaw plugin is installed and configured locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
