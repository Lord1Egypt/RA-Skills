## Description:

Tracks countdown dates so users can plan schedules around holidays, anniversaries, deadlines, and other dated events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rain-lei](https://clawhub.ai/user/rain-lei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read or maintain simple countdown entries and report remaining or elapsed days for named dates. It is suited to lightweight schedule reminders where local JSON storage is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Countdown names and dates are stored in a local JSON file and may reveal personal or sensitive events.

Mitigation: Avoid storing sensitive personal dates and restrict file access according to the user's local environment.

Risk: Manual edits can delete entries or overwrite an existing countdown when a name is reused.

Mitigation: Back up the JSON file before bulk edits and review names for duplicates before saving changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rain-lei/skills/date-count)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses named date entries stored in a local JSON file; the artifact contains no executable code.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
