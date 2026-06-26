## Description: <br>
Provides MaxCompute SQL generation guidance for AI agents, covering text-to-SQL principles, MaxCompute dialect differences, common query patterns, and ODPS error diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to generate, debug, and migrate MaxCompute or ODPS SQL using dialect-specific syntax rules, query templates, and error recovery guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can be incorrect, expensive, or access-sensitive if users run it without reviewing schema assumptions, partition filters, joins, SET changes, or write operations. <br>
Mitigation: Review generated SQL before execution, confirm table schema and permissions, check partition and join behavior, and avoid blind retries of non-idempotent DML such as INSERT INTO, MERGE, UPDATE, or DELETE. <br>


## Reference(s): <br>
- [Text2SQL General Generation Principles](references/text2sql_principles.md) <br>
- [MaxCompute SELECT Dialect Rules](references/maxcompute_select_guide.md) <br>
- [MaxCompute SQL Query Pattern Templates](references/sql_query_patterns.md) <br>
- [MaxCompute SQL Error Recovery Guide](references/sql_common_errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JSON or Markdown with MaxCompute SQL, explanations, assumptions, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is documentation-only and does not execute database operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
