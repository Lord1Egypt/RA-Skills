## Description:

EventKit integration patterns, permission handling, zero-width character steganography, and batch operations for macOS/iOS apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building macOS or iOS applications use this skill for EventKit reminders and events integration, permission handling, calendar management, batch operations, and bidirectional sync patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples request broad EventKit reminder and event permissions, which can expose more calendar data than a specific app workflow needs.

Mitigation: Request only the EventKit permissions required for the app feature, explain the purpose to users, and avoid event access when reminder-only access is sufficient.

Risk: The skill teaches invisible identity markers in reminder notes, which can surprise users and make stored metadata hard to inspect or remove.

Mitigation: Use invisible note markers only with explicit user opt-in, document what is stored, and provide a way to remove or migrate the markers.

Risk: Batch deletion and duplicate-purge patterns can remove important reminders or local task records if identifiers, sync state, or duplicate detection are wrong.

Mitigation: Add confirmation, backups, dry-run logging, or undo safeguards before deleting reminders or local records, and test deletion flows against non-production calendars.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/eventkit-integration)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with Swift and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
