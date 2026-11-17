## Description:

Builds day-by-day exam study plans with prioritized topics, spaced reviews, daily load limits, and feasibility checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Students use this skill to turn exam dates, available hours, and syllabus topics into a prioritized study timetable with spaced reviews and replanning after missed sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exam dates, topics, and study progress are saved in a local JSON plan file that may be updated or reset.

Mitigation: Choose a dedicated --store path, back up the plan before resetting it, and review changes to the timetable.

## Reference(s):

- [Exam Timetable Architect method](references/method.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/exam-timetable-architect)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, JSON]

**Output Format:** [Text study schedules and progress summaries; local JSON plan file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily study blocks, review reminders, feasibility warnings, and progress tracking.]

## Skill Version(s):

1.0.1 (source: server release; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
