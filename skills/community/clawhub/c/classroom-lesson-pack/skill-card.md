## Description:

Generates reviewable lesson plans, interactive questions, assignments, and differentiated teaching suggestions from course goals, duration, audience, and difficulty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, trainers, and workshop facilitators use this skill to turn teaching goals and class constraints into structured lesson-plan drafts, classroom activities, homework, and differentiated teaching suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lesson-plan drafts may be incomplete, inaccurate, or mismatched to a class when the input omits goals, duration, audience, or difficulty.

Mitigation: Have an educator review the draft before classroom use and resolve the listed missing information before treating it as final.

Risk: Lesson inputs may contain student, personal, or sensitive classroom information.

Mitigation: Redact sensitive student or personal data before use, as recommended by the security guidance.

Risk: The optional local script can write an output file and contains dormant audit modes that could scan broader filesystem content if repurposed.

Mitigation: Use the packaged structured_brief mode for normal lesson drafting, prefer stdout or dry-run for review, and separately review any broad filesystem scanning use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/classroom-lesson-pack)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Files]

**Output Format:** [Structured Markdown by default, with optional JSON from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local script can print to stdout or write an output file when --output is provided.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
