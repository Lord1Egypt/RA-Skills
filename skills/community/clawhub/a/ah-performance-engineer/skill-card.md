## Description:

This skill provides performance engineering guidance for system profiling, load testing, bottleneck analysis, and optimization across the technology stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan performance analysis, profiling, load testing, monitoring, capacity planning, and optimization work across application, database, frontend, and host layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database optimization examples include DDL and system-setting changes that can affect live databases.

Mitigation: Validate SQL in a non-production environment, confirm compatibility with the target database, back up current state, and prepare a rollback plan before use.

Risk: Linux tuning examples include host-level settings that can persistently change system behavior.

Mitigation: Have an operator review commands, test them outside production, record original settings, and apply changes only with a tested rollback path.

## Reference(s):

- [Performance Engineer examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-performance-engineer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory performance-engineering plans, examples, and tuning guidance for human review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
