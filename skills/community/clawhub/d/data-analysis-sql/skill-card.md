## Description: <br>
A data engineering skill for multi-engine SQL writing, migration, optimization, warehouse modeling, ETL planning, data-quality analysis, metric design, and Markdown knowledge-base documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whiskeyforsun](https://clawhub.ai/user/whiskeyforsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, analysts, and developers use this skill to design and revise SQL, model warehouse layers, define business metrics, troubleshoot data-quality issues, and generate Markdown documentation for schemas, migrations, and knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad SQL and documentation triggers may activate the skill for ambiguous or generic document requests. <br>
Mitigation: Review ambiguous activations before allowing the skill to act on general documentation tasks. <br>
Risk: Documentation generation can write to user-specified output paths and may replace existing Markdown content. <br>
Mitigation: Confirm output filenames and paths before generating documentation, and review generated files before relying on them. <br>
Risk: Generated SQL and data-modeling guidance may encode incorrect assumptions about schemas, metrics, tenants, or deletion flags. <br>
Mitigation: Validate generated SQL against the target schema, metric definitions, and sample query results before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whiskeyforsun/data-analysis-sql) <br>
- [README](README.md) <br>
- [SQL guide](references/sql-guide.md) <br>
- [Join rules](references/join-rules.md) <br>
- [SQL pitfalls](references/sql-pitfalls.md) <br>
- [Business metrics](references/business-metrics.md) <br>
- [Schema guide](references/schema-guide.md) <br>
- [Multi-engine SQL](references/multi-engine.md) <br>
- [Pipeline patterns](references/pipeline-patterns.md) <br>
- [Data quality](references/data-quality.md) <br>
- [Data analysis patterns](references/data-analysis-patterns.md) <br>
- [Knowledge base](references/knowledge-base.md) <br>
- [Documentation guide](references/doc-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL snippets, generated Markdown files, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or update local Markdown documentation when the user supplies output paths.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
