## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, query, link, and validate typed local ontology objects for structured memory, task tracking, planning, and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation describes validation and secret-handling protections that the security evidence says are not fully enforced by the code.

Mitigation: Do not store passwords, tokens, API keys, or other secrets in the ontology graph; use secret references only and review or audit graph mutations after use.

Risk: Ontology graph changes may persist incorrect or unsafe state if relied on without review.

Mitigation: Run validation and inspect the graph after mutations before using the stored state for planning, task execution, or cross-skill decisions.

## Reference(s):

- [Ontology Schema Reference](references/schema.md)
- [Query Reference](references/queries.md)
- [ClawHub skill page](https://clawhub.ai/tihuaqin-commits/skills/fox-ontology)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline Python and shell command examples; runtime operations write JSONL and YAML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
