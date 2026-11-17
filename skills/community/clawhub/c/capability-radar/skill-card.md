## Description:

Detects and records capability gaps, repeated failure patterns, rule conflicts, workaround use, and user corrections so future agent sessions can prioritize skill or rule improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dottythehomeless](https://clawhub.ai/user/dottythehomeless)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use Capability Radar to log tool failures, capability boundaries, repeated request patterns, rule conflicts, workaround use, and user corrections into a structured memory queue for later skill or rule evolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived incident logs may store names, secrets, internal URLs, customer data, or other sensitive context in persistent memory.

Mitigation: Redact sensitive details before writing memory entries, especially in shared or sensitive workspaces.

Risk: Persistent improvement queues can steer future sessions toward skill or rule changes without enough scoping or minimization.

Mitigation: Require explicit approval before writing memory entries and treat stored records as evidence, not instructions.

## Reference(s):

- [Capability Radar ClawHub Skill Page](https://clawhub.ai/dottythehomeless/skills/capability-radar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown memory entries with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent records should be redacted and reviewed before storage in shared or sensitive workspaces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
