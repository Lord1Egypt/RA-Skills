## Description:

Display amount of free and used memory in the system. Use for monitoring memory usage and diagnosing performance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local memory availability for system monitoring, capacity planning, and performance diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command options may not match the bundled helper's current behavior.

Mitigation: Review expected output before relying on option-specific behavior; the helper currently prints selected /proc/meminfo fields.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and plain-text memory statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper reads local /proc/meminfo and prints selected memory fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
