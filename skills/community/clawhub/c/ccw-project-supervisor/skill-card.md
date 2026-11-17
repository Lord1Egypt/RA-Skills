## Description:

Supervises software project execution with OpenClaude and Claude Code Workflow by selecting the right workflow stage, checking backlog quality, validating dependency order, and recommending the next CCW step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majmunu](https://clawhub.ai/user/majmunu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to supervise planning, issue breakdown, queue validation, and execution-readiness for greenfield or existing software projects using CCW.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend a CCW execution stage before a project queue is sufficiently clear.

Mitigation: Use the skill's queue-clarity and dependency-order checks before following execution recommendations.

Risk: Planning guidance may be incorrect or drift beyond the provided backlog and constraints.

Mitigation: Review stage rationale, validation notes, and proposed CCW prompts against the project source materials before acting.

## Reference(s):

- [CCW Project Supervisor on ClawHub](https://clawhub.ai/majmunu/skills/ccw-project-supervisor)
- [Majmunu Publisher Profile](https://clawhub.ai/user/majmunu)
- [Phase Checklists](references/phase-checklists.md)
- [Engineering Order Reference](references/engineering-order.md)
- [Prompt Templates](references/prompt-templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with copy-ready CCW command prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stage assessment, validation notes, exit criteria, and the recommended next CCW command.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
