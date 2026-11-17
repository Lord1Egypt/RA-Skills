## Description:

Manage Apple Reminders from the command line on macOS. List, add, edit, complete and delete reminders, filter by due date, with JSON output for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopaljigaur](https://clawhub.ai/user/gopaljigaur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this CLI to inspect and manage reminders in Apple Reminders on macOS, including creating tasks, updating due dates and priorities, and marking or deleting reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied release is missing JXA runtime scripts, so its security assessment is incomplete.

Mitigation: Verify the complete matching npm package before granting it access to Reminders.

Risk: Reminder results can expose private notes across multiple lists, and deletion cannot be undone.

Mitigation: Select a specific list when appropriate and inspect the target with `arcli show <id>` before deleting it.

## Reference(s):

- [Apple Reminders CLI on ClawHub](https://clawhub.ai/gopaljigaur/skills/arcli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [Shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on macOS and requires permission to access Reminders; flag operations also require Automation access to Reminders.app.]

## Skill Version(s):

0.1.2 (source: package.json and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
