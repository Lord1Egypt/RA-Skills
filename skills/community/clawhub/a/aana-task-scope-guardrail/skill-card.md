## Description:

Ensures an agent performs only requested tasks using relevant data, stops when complete, and avoids expanding beyond the user's original scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw-style agents within the current user request, limit data use to relevant context, and require approval before scope expansion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured external checker could receive sensitive or unrelated task context if payloads are not minimized.

Mitigation: Send only the redacted scope-review fields described by the skill and use only trusted user- or administrator-approved checker connectors.

Risk: The skill provides instruction guidance rather than enforcing behavior by itself.

Mitigation: Use it as a local review boundary and require explicit approval before broader work, private-data access, external actions, or post-completion follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-task-scope-guardrail)
- [Artifact README](artifact/README.md)
- [Task scope gate schema](artifact/schemas/task-scope-gate.schema.json)
- [Redacted task scope gate example](artifact/examples/redacted-task-scope-gate.json)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, configuration]

**Output Format:** [Markdown instructions with an optional structured scope-gate payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, write files, call services, or persist memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
