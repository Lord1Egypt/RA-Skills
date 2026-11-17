## Description:

Create, update, and query typed entities and relations such as Person, Project, and Task in a verifiable knowledge graph with validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain structured local memory as typed entities and relations, then query or traverse that graph for project, task, person, and knowledge-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local graph memory that may capture sensitive, private, or regulated information.

Mitigation: Avoid storing passwords, API keys, tokens, private messages, or regulated personal data until secret-field rejection, file permission hardening, and deletion/update controls are implemented.

Risk: The security evidence says promised validation and secret protections are not fully enforced.

Mitigation: Review stored fields before use, scan releases before deployment, and add validation and secret-handling controls before using the graph for sensitive workflows.

## Reference(s):

- [Ontology Schema Reference](artifact/references/schema.md)
- [Query Reference](artifact/references/queries.md)
- [ClawHub Skill Page](https://clawhub.ai/biociao/skills/agent-ontology)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with CLI examples, JSON graph records, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and queries append-only JSONL records in a local ontology graph.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
