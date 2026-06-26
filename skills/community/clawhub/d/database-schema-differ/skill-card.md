## Description: <br>
Compare database schemas across environments, generate migration scripts, and track schema evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and CI/CD maintainers use this skill to compare database schemas across environments, generate migration SQL, capture snapshots, and detect schema drift before changes reach production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle database connection details for live schema comparisons. <br>
Mitigation: Use environment variables or a secrets manager, avoid putting real passwords in command lines, and limit credentials to the minimum database privileges needed. <br>
Risk: Generated migration SQL can include destructive or constraint-changing statements. <br>
Mitigation: Inspect generated SQL for DROP, ALTER, and constraint changes; back up data; and apply migrations through the normal review and release process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Derick001/database-schema-differ) <br>
- [Derick001 publisher profile](https://clawhub.ai/user/Derick001) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts may include SQL migration scripts, JSON reports, and HTML visual diffs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and database-specific dependencies; generated SQL should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
