## Description: <br>
SQL智能助手，支持SQL执行、重写优化、质量分析、数据分析、智能补全、Schema查询、批量执行、数据导入导出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and database operators use this skill to run and inspect SQL through dbskiter, including execution, rewrite and quality analysis, schema exploration, completion, batch execution, and data import or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run, import, export, and batch-execute database operations without clear safety checks. <br>
Mitigation: Use read-only or least-privilege database aliases by default and require human confirmation before write, import, export, batch, schema-changing, or broad SELECT operations. <br>
Risk: The skill depends on the local dbskiter binary and database configuration selected by the operator. <br>
Mitigation: Verify the dbskiter binary and configuration before use, especially for production databases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-sql-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline bash and SQL snippets; file outputs may be CSV, JSON, or SQL when dbskiter export/import workflows are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured dbskiter database alias and permissions appropriate to the requested SQL operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
