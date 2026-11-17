## Description:

Use when designing a new CLI, reviewing an existing CLI, or resolving uncertainty about a CLI's role, user type, interaction form, statefulness, risk profile, or human-vs-machine surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangnov](https://clawhub.ai/user/wangnov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to design or review command-line interfaces by classifying the CLI's role, user type, interaction form, statefulness, risk profile, and primary versus secondary surfaces. It helps produce concise design blueprints, structured reviews, and implementation direction for human-facing, machine-facing, and hybrid CLIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: During a CLI review, an agent may inspect project files or CLI behavior and could be asked to run target commands.

Mitigation: Keep normal approval and sandbox policies in place before running any target CLI commands, especially for deployment or agent-runtime tools.

Risk: The skill can produce design or review guidance that may be incomplete or misclassified if the target CLI evidence is sparse.

Mitigation: Review generated classifications, risk ladders, and machine-surface recommendations against the actual CLI help, docs, code, tests, and runtime behavior before implementation.

## Reference(s):

- [CLI Design Framework skill page](https://clawhub.ai/wangnov/skills/cli-design-framework)
- [Taxonomy](references/taxonomy.md)
- [Output Templates](references/output-templates.md)
- [Classification Examples](references/classification-examples.md)
- [Design Blueprint Example](examples/design-blueprint-example.md)
- [Review Example](examples/review-example.md)
- [Anti-Patterns](examples/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown prose with structured sections and occasional inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are concise, classification-first design blueprints or reviews; longer templates are used when ambiguity, risk, or an explicit user request justifies them.]

## Skill Version(s):

1.0.2 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
