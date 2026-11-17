## Description:

Turn school or university timetables into checked .ics calendars for Apple Calendar, Google Calendar, and similar apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidai-1999](https://clawhub.ai/user/davidai-1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to normalize school or university timetable inputs, verify coverage against source material, resolve calendar-specific ambiguities, and generate deterministic .ics exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated calendar files may be incorrect when manifests come from untrusted sources or omit school-specific timezone, week-1, or period-time details.

Mitigation: Use manifests from trusted sources, provide the actual timezone and schedule anchors, verify coverage against the source timetable, and inspect generated .ics files before importing.

Risk: The server security summary notes a narrow input-validation weakness in the calendar generator.

Mitigation: Avoid relying on generated .ics files from untrusted manifests until ICS validation is tightened, and review outputs before calendar import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidai-1999/skills/course-schedule-export)
- [Manifest Schema](artifact/references/manifest-schema.md)
- [Coverage Schema](artifact/references/coverage-schema.md)
- [Pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON manifests and generated .ics calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided authoritative timetable inputs, period times, timezone, and week-1 anchor when recurring classes are present.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
