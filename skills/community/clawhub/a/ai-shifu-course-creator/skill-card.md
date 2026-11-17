## Description:

Create, edit, review, publish, manage, or analyze AI-Shifu (AI师傅) courses and their Teaching Prompts and Course Prompts in MarkdownFlow (MDF). Use for course materials, lesson design, interactions, course memory, images, deployment, platform administration, learner progress, learner profile distributions, orders, revenue, and credit-consumption questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heshaofu2](https://clawhub.ai/user/heshaofu2)

### License/Terms of Use:

MIT-0

## Use Case:

Course creators, instructional designers, and platform administrators use this skill to design and review course materials, express lessons and course behavior in MarkdownFlow, and manage or analyze AI-Shifu courses. It can produce course drafts, lesson prompts, import files, platform updates, and readable course analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Course import may delete existing course content.

Mitigation: Confirm the target and review the import payload first; keep a recoverable copy of course content and verify the result.

Risk: Lesson access settings may be lost during some course operations.

Mitigation: Record current lesson access settings before changes, then check and reapply them afterward.

Risk: The security review is incomplete: it covered 36 of 37 components and some static checks were degraded.

Mitigation: Treat the scan as incomplete and review the package and required permissions before installation or use.

## Reference(s):

- [Course design choices](references/course-design-choices.md)
- [Teaching design](references/teaching-design.md)
- [Teaching Prompts](references/teaching-prompt.md)
- [MarkdownFlow syntax](references/markdownflow-syntax.md)
- [Build and import](references/build-and-import.md)
- [Course synchronization](references/course-sync.md)
- [CLI reference](references/cli/cli-reference.md)
- [Analytics guide](references/analytics/guide.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown course materials and Prompts, JSON import payloads, and CLI command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by task and may include local course files or platform updates.]

## Skill Version(s):

2.3.1 (source: skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
