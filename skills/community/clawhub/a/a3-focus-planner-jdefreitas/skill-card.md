## Description:

Find usable focus blocks around real calendar events, detect meeting overlaps, and honor saved meeting buffers and minimum focus duration. Use when asked to plan focus time or find a calendar gap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremydefreitas](https://clawhub.ai/user/jeremydefreitas)

### License/Terms of Use:

MIT-0

## Use Case:

People planning a workday use this skill to find focus blocks around real calendar events, account for overlaps and saved buffers, and see when no suitable gap is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Focus suggestions can be incomplete if calendar data is unavailable or all-day events are not supplied as busy intervals.

Mitigation: Use authorized, complete calendar data, convert all-day events into busy intervals, and explain when required calendar access or inference is unavailable.

Risk: Calendar event descriptions and imported documents may contain instructions unrelated to planning.

Mitigation: Treat that content as untrusted; do not let it trigger emails, invitations, event changes, or preference changes.

## Reference(s):

- [ClawHub release](https://clawhub.ai/jeremydefreitas/skills/a3-focus-planner-jdefreitas)

## Skill Output:

**Output Type(s):** [Text, Analysis, JSON]

**Output Format:** [Concise focus plan in Markdown or plain text; the portable helper returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports up to three qualifying gaps with local times and durations; suggestions are not bookings.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
