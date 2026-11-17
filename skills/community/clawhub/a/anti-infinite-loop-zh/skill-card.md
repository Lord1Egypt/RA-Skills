## Description:

反无限循环守护 helps agents detect repeated actions, enforce stop conditions, track progress, and limit runtime to reduce unproductive execution loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a Chinese-language helper for adding simple loop limits, repeated-action checks, progress checks, and runtime limits to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loop-guard checks may be treated as a complete enforcement system even though the security guidance describes the claims as lightweight.

Mitigation: Review generated limits and progress checks before deployment, and pair them with runtime monitoring or platform controls for high-impact workflows.

Risk: Repeated-action or progress heuristics may stop useful work too early or allow unproductive work to continue.

Mitigation: Tune max iterations, timeout, and progress thresholds for the target workflow and validate behavior with representative tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/anti-infinite-loop-zh)
- [Publisher profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance with simple watchdog status metrics and configurable iteration, progress, and time limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
