## Description:

Manage Apple Reminders via the `remindctl` CLI on macOS (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users on macOS use this skill to inspect and manage Apple Reminders through `remindctl`, including list management, date-filtered views, reminder creation, edits, completion, deletion, and scripting output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder edits, completions, renames, deletes, and bulk operations can modify or remove personal data if the target is vague or wrong.

Mitigation: Confirm the exact reminder IDs, list names, or affected targets with the user before destructive or state-modifying commands.

Risk: Reminder content can contain private schedule, task, and note data that should not be transmitted externally.

Mitigation: Keep reminder output local, scope reads to the requested list or date range, and do not pipe `remindctl` output to webhooks or other network destinations.

Risk: Installing and authorizing `remindctl` grants a third-party CLI access to read and modify Apple Reminders on the Mac.

Mitigation: Verify trust in the `steipete/tap/remindctl` Homebrew tap and review macOS Reminders permissions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/apple-reminders-hardened)
- [remindctl homepage](https://github.com/steipete/remindctl)
- [Faberlens safety evaluation](https://faberlens.ai/explore/apple-reminders)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown with inline shell commands and optional JSON/plain `remindctl` output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS and requires the `remindctl` binary with Apple Reminders permission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
