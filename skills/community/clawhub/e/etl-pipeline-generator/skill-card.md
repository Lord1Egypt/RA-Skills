## Description: <br>
Generate automated ETL pipelines for transforming and loading data into graph databases or knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design repeatable ETL workflows that extract data from files, APIs, databases, or streams, transform it into graph-ready structures, and load it into knowledge graph storage systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ETL pipelines may read sensitive source data or write, overwrite, or delete target graph data. <br>
Mitigation: Review generated ETL code and configuration before use, test with staging data first, require explicit confirmation for production writes or deletes, and keep backups or rollback plans. <br>
Risk: Pipeline configurations may require credentials for APIs, databases, streams, or graph stores. <br>
Mitigation: Do not embed secrets in generated configs; use secret stores or environment-based credentials with least-privilege access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/etl-pipeline-generator) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [ETL Pipeline Design Patterns](artifact/references/pipeline-patterns.md) <br>
- [ETL Pipeline Examples](artifact/examples/example-pipelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, YAML configuration, DAG descriptions, generated code snippets, and monitoring or alerting settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated ETL artifacts should be reviewed before execution against production data sources or graph databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
