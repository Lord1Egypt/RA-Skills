## Description: <br>
Generate graph database loaders and triple mappings from CSV datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to convert CSV datasets into graph-ready nodes, relationships, triples, schemas, and loader scripts for knowledge graph or graph database workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Neo4j loaders, RDF mappings, and import configurations may write to downstream databases or use incorrect paths, database names, or credentials if executed without review. <br>
Mitigation: Review generated outputs before running them, use least-privilege database credentials, confirm target paths and database names, and test against a non-production database or backup first. <br>
Risk: Automatic entity and relationship inference may produce incorrect graph structure for ambiguous CSV schemas. <br>
Mitigation: Prefer explicit or hinted mappings for production workflows and validate the generated schema, nodes, relationships, and duplicate handling against representative sample data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/csv-graph-loader-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/fisa712) <br>
- [ClawHub Homepage](https://clawhub.com) <br>
- [CSV Loader Design Patterns](references/loader-patterns.md) <br>
- [CSV Graph Loader Examples](examples/example-loaders.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated Cypher, RDF Turtle, JSON, CSV node and edge tables, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce database import scripts and mapping configurations that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
