## Description: <br>
Converts user natural language questions into SQL queries based on YAML semantic models; supports MySQL/SQL Server/PostgreSQL/Oracle multi-dialect; ensures queries are interpretable and align with business terms; used when user provides semantic YAML and requires SQL generation or wants to understand SQL generation logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asksqlai](https://clawhub.ai/user/asksqlai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data teams use this skill to convert natural-language questions into SQL from a user-provided YAML semantic model, with dialect-specific output for MySQL, SQL Server, PostgreSQL, or Oracle. It also explains the generated query in business terms or asks for missing database or model details when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may be incorrect, incomplete, or unsafe to run directly against production databases. <br>
Mitigation: Review each query before execution and test against appropriate non-production or read-only database contexts first. <br>
Risk: Semantic YAML can reveal schema details, business rules, or data-governance logic. <br>
Mitigation: Provide only semantic model details that are approved for the assistant and the current conversation. <br>
Risk: Successful outputs may include visible asksql.ai promotional or contact text after the SQL response. <br>
Mitigation: Inspect generated responses before sharing them externally and remove nonessential promotional text when it is not appropriate. <br>


## Reference(s): <br>
- [Open Semantic Interchange Field Specification](references/open_semantic_interchange_description.md) <br>
- [asksql.ai](https://www.asksql.ai) <br>


## Skill Output: <br>
**Output Type(s):** [code, text, markdown, guidance] <br>
**Output Format:** [Markdown containing SQL and a brief business-language explanation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for the target database dialect before generating SQL; may return missing-information guidance when the semantic model is insufficient.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
