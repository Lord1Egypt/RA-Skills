## Description:

Builds a dated editorial calendar with owners, channels and the US seasonal moments mapped to the weeks they fall in. Use when the user asks for content calendar template, editorial calendar planner, monthly content schedule. For US in-house content managers and one-person marketing teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US in-house content managers and one-person marketing teams can use this skill to draft a basic dated weekly outline for editorial planning. The generated plan needs manual completion and review before it is shared or relied on.

### Deployment Geography for Use:

United States (US-focused calendar guidance)

## Known Risks and Mitigations:

Risk: The supplied CSV template does not match the planner's input parser, so its fields may not be applied to the generated plan.

Mitigation: Review the output and complete or correct the plan manually; do not assume CSV values were used.

Risk: The planner writes a file named plan.md and can overwrite an existing file with that name.

Mitigation: Choose a dedicated output folder and check for an existing plan.md before running it.

Risk: The optional Windows app is a separate unsigned download and has not been established as safe by a matching publisher-provided hash alone.

Mitigation: The planner does not need the app; avoid it unless it receives a separate security review.

## Reference(s):

- [Running a US editorial calendar](references/editorial-calendar.md)

## Skill Output:

**Output Type(s):** [Markdown, Planning guidance]

**Output Format:** [Markdown dated outline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A basic weekly outline over a 90-day horizon; manually check dates and complete the plan.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
