## Description:

Checks a fixed Discord dispatch parent channel for recently created or clearly polluted thread titles, renames up to three noncompliant threads to a standard pattern, and stays silent unless a final failure or recovery notice is required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations maintainers use this skill to run a low-noise Discord thread naming backstop for a specific guild and dispatch channel. It helps inspect recent thread titles, skip compliant or historical threads, retry Discord API failures, and issue only necessary P2 or RESOLVED notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An installed agent with Discord permissions can read the specified dispatch channel, rename a small number of recent thread titles, and post limited failure or recovery notices.

Mitigation: Install only for the intended dispatch workflow and require confirmation of the guild, channel, and scope before allowing renames for informal requests.

## Reference(s):

- [Dispatch Thread Rename Notification Templates](references/dispatch-thread-rename-notification-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/can4hou6joeng4/skills/discord-thread-naming-backstop-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with plain-text notification templates and Discord action parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal runs should be silent; failure or recovery notices are limited to one message per thread per run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
