## Description:

DingJi smart course design for higher mathematics. Provides task-driven learning paths, adaptive diagnosis, Bloom high-level cognition training. Trigger: design math course, create teaching plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, instructional designers, and agent operators use this skill to generate higher mathematics course plans, learning paths, diagnostics, practice workflows, and teaching feedback grounded in Bloom taxonomy and immersive learning patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to write persistent memory, schedule reminders, use subagents, upload content, send messages, or run exec/Python commands without clear consent boundaries.

Mitigation: Require explicit user confirmation before any Memory write, cron setup, upload, external message, subagent delegation, or exec/Python run.

Risk: Generated higher-math diagnostics, course plans, and feedback can be incomplete or pedagogically inappropriate for a real learner.

Mitigation: Have a qualified educator review generated plans, assessments, and learner recommendations before using them in instruction.

Risk: The source skill is primarily Chinese and may produce output in an unintended language for some users.

Mitigation: Ask for the preferred output language before generating teaching materials or learner-facing feedback.

## Reference(s):

- [DingJi Course Design on ClawHub](https://clawhub.ai/daigxok/skills/dingji-course-design)
- [Higher Mathematics Error Pattern Library](artifact/references/error-patterns.md)
- [Higher Mathematics Knowledge Graph](artifact/references/math-knowledge-graph.md)
- [Mathematics Task SOP Template Library](artifact/references/task-templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown with structured learning paths, diagnostic tables, task templates, and occasional code or shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include course plans, learner profiles, review schedules, assessment rubrics, visualization prompts, and agent workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
