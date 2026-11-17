## Description:

Provides a structured bug-fixing workflow that guides an agent to analyze reported bugs, inspect module logic and syntax, compare behavior with official documentation, check performance, and write a Fix Report after repairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyahui](https://clawhub.ai/user/miyahui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill when a user reports a bug and they need the agent to move through diagnosis, source inspection, documentation comparison, performance review, transparent user communication, and post-fix reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt the agent to inspect repository or project files while debugging.

Mitigation: Use it only with repositories and project files that are appropriate for agent review.

Risk: Fix Report notes or reused debugging knowledge may retain project-specific details.

Mitigation: Keep reports and any knowledge-base entries scoped to the relevant project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miyahui/skills/bug-reflection)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance and Fix Report notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bug analysis, inspected modules, documentation comparisons, performance observations, repair attempts, final solution notes, and lessons learned.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
