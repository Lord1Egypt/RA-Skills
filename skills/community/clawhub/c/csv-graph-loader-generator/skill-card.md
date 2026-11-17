## Description:

Generate graph database loaders and triple mappings from CSV datasets. Converts tabular CSV data into graph-ready nodes, edges, and triples for graph databases or knowledge graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to convert CSV datasets into graph-ready structures for Neo4j, RDF triple stores, property graphs, and knowledge graph workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated database/import files may contain unsafe or incorrect identifiers, values, or relationships when source CSV data is untrusted.

Mitigation: Review generated Cypher, Turtle, CSV, and JSON outputs, test imports in a non-production database, validate or escape untrusted identifiers and values, and use least-privileged database credentials.

Risk: Automatic relationship inference may create an inaccurate graph model for complex or ambiguous CSV schemas.

Mitigation: Use semi-automated hints or explicit mapping rules, validate sample outputs, and check for duplicate nodes or relationships before production imports.

## Reference(s):

- [CSV Loader Design Patterns](references/loader-patterns.md)
- [CSV Graph Loader Examples](examples/example-loaders.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/csv-graph-loader-generator)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, generated loader scripts, mapping configuration, and JSON, Turtle, or Cypher examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated database and import files should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
