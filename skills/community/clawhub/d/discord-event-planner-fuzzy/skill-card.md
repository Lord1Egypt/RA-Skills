## Description:

Plan and coordinate events in Discord. Use when users ask to create, schedule, or manage events, plan meetups, organize activities, set up reminders, or track RSVPs in Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Discord community moderators and organizers use this skill to create scheduled events, list upcoming events, manage RSVP status, show event details, and cancel events while keeping event data in a local JSON file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event data is written to a local events.json file relative to the current working directory, so running the script from the wrong location can create or modify an unexpected file.

Mitigation: Run the script from the intended workspace and review the events.json location before use.

Risk: Canceling an event removes its record from the local event store.

Mitigation: Confirm the event ID before canceling and keep a backup when event history needs to be retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/discord-event-planner-fuzzy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with Discord command examples and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains event state in a local events.json file relative to the current working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
