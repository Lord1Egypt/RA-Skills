## Description:

Feishu Room Booking helps agents configure tenant room catalogs, query Feishu meeting-room availability, book or rebook rooms, manage room preferences, poll waitlists, and maintain workspace timelines for Feishu users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushibang](https://clawhub.ai/user/qiushibang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and their agents use this skill to find and reserve Feishu meeting rooms, import tenant-specific room resources, and manage preferences or waitlists for scheduled meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires current-user Feishu calendar access, including attendee reads and calendar or room-resource writes.

Mitigation: Install only after reviewing the requested Feishu permissions and confirming the user is comfortable granting calendar access.

Risk: Automatic rebooking and waitlist polling can submit room bookings without a fresh confirmation in some flows.

Mitigation: Require explicit user opt-in before enabling automatic rebooking or waitlist polling, and verify room RSVP state before reporting success.

Risk: Local JSON files may contain employee IDs, meeting summaries, room choices, event IDs, and workplace-location history.

Mitigation: Review, protect, and periodically remove generated local JSON state files according to the user's data-handling requirements.

Risk: The server security verdict is suspicious because the skill can read calendar details, store workplace data locally, and write calendar resources.

Mitigation: Review the skill before deployment and use dry-run or status commands before enabling write-capable workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiushibang/skills/feishu-room-booking)
- [Publisher profile](https://clawhub.ai/user/qiushibang)
- [Room mapping catalog](references/room-mapping.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line output, including JSON or table-formatted room and booking results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu current-user authorization through lark-cli and local JSON state files for tenant setup, preferences, waitlists, and workspace history.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
