## Description:

Manage Apple Reminders via the `remindctl` CLI on macOS, including listing, adding, editing, completing, and deleting reminders with list, date-filter, JSON, and plain-text output support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to have an agent help manage Apple Reminders through `remindctl` commands. It is intended for reminder viewing, creation, editing, completion, deletion, list management, date filtering, and scripting-oriented output on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and force-delete operations may remove reminders or lists from Apple Reminders data.

Mitigation: Review each proposed command before approval, especially delete, force-delete, and list deletion commands.

Risk: The skill requires local macOS Reminders access through `remindctl`.

Mitigation: Install it only on Macs where agent-assisted Reminders management is intended, and grant Reminders permission deliberately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tigertamvip/skills/apple-reminders-1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, the `remindctl` binary, and Reminders permission on the Mac where commands run.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
