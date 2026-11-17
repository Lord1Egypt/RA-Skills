## Description:

Cal-Candy helps an agent manage a local Markdown calendar by adding, listing, viewing, reminding on, and deleting calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage time-bound tasks in a local Markdown calendar, including creating events, checking current or upcoming schedules, configuring reminders, and deleting obsolete entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and delete local calendar entries.

Mitigation: Confirm the user's intent before event creation or deletion, and keep MDCAL_DIR limited to a dedicated calendar directory.

Risk: Event titles and descriptions are written into Markdown files.

Mitigation: Avoid passing untrusted multiline text as event titles or descriptions, and review generated entries before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/cal-candy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Markdown files and a reminders JSON file in the configured calendar directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
