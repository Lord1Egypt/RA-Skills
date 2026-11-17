## Description:

Generates module structures, unit objectives, assignments, milestones, and common learner friction points for creator-focused courses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Course creators, educators, and knowledge-product teams use this skill to turn a course topic, audience, goals, and duration into a review-ready outline with objectives, assignments, milestones, and items needing confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can optionally run a local Python script on user-provided files.

Mitigation: Review the bundled script before enabling shell execution in high-trust workspaces, and run it only on intended local inputs.

Risk: Course inputs may contain private or sensitive planning material that will be summarized into generated output.

Mitigation: Redact sensitive material first and provide only content that is appropriate to appear in a course draft.

Risk: Generated outlines are drafting aids and may be mistaken for guaranteed learner outcomes or formal instructional-design approval.

Mitigation: Treat the output as a review-ready draft, confirm missing assumptions, and obtain appropriate human review before publishing or using it as a final curriculum.

## Reference(s):

- [Creator Course Outline on ClawHub](https://clawhub.ai/52yuanchangxing/skills/creator-course-outline)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Structured output specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown by default, with an optional JSON mode from the bundled local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are structured as course goals, module structure, unit goals, assignments, milestones, common learner friction points, pending confirmations, and next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
