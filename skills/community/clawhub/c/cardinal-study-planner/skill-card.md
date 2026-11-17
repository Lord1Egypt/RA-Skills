## Description:

Plan study blocks around supplied busy intervals, detect calendar overlaps, preserve meeting buffers and breaks, and report study time that cannot fit. Use for finding study time or checking whether a study goal fits a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meethdavda](https://clawhub.ai/user/meethdavda)

### License/Terms of Use:

MIT-0

## Use Case:

Learners can use the skill to plan study sessions around known commitments, check for overlapping events, and see when a study goal cannot fit in the available time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the helper executes a local Python script.

Mitigation: Review its requested access and use it only in an environment where you are comfortable running the listed executable.

Risk: A plan may be incomplete if busy times or unavailable periods are missing.

Mitigation: Ask for missing schedule information and do not treat an unknown calendar as empty.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/meethdavda/skills/cardinal-study-planner)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON study plan with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proposed study blocks, conflicts, available gaps, and unscheduled minutes; does not modify the calendar.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
