## Description: <br>
Design data models for construction projects. Create entity-relationship diagrams, define schemas, and generate database structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction data practitioners, developers, and project teams use this skill to design project data models, define construction entities and relationships, generate database schemas, and validate model structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use filesystem access for project files and export paths. <br>
Mitigation: Grant access only to intended project files and review export paths before use. <br>
Risk: Generated SQL DDL may contain incorrect or unsafe identifiers for a real database. <br>
Mitigation: Review and validate generated SQL identifiers and schema changes before executing them. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/data-model-designer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with generated SQL DDL, JSON Schema, Mermaid ER diagrams, and validation notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference user-provided project data and local file paths when the user grants filesystem access.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
