## Description: <br>
Provides guidance for avoiding Railway PostgreSQL connection pool exhaustion by checking pool status, using short-lived connections, closing connections promptly, and handling "too many clients" errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when running local scripts or diagnostics against Railway PostgreSQL databases to avoid exhausting connection pools and recover from "too many clients" errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad process-kill commands may terminate unrelated local work or development services. <br>
Mitigation: Verify the exact process before stopping it and prefer graceful shutdowns before force-kill commands. <br>
Risk: Database session termination commands may disrupt production service or another user's active work. <br>
Mitigation: Verify the Railway project, database, and session target; prefer read-only connection checks and reserve session termination for reviewed emergency use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urbantech/database-query-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, SQL, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory database-safety guidance; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
