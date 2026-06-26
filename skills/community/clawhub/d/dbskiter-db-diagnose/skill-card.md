## Description: <br>
Helps agents use dbskiter to diagnose SQL, slow queries, index opportunities, performance snapshots, and bottlenecks for MySQL, Oracle, and PostgreSQL databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and operations engineers use this skill to triage database performance issues, inspect slow SQL, review lock and session conditions, and collect optimization recommendations through dbskiter commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database diagnostics can expose sensitive SQL literals, schema names, usernames, session details, and lock information. <br>
Mitigation: Use read-only or least-privileged database accounts and redact sensitive values before sharing diagnostic output. <br>
Risk: Broad diagnostics may inspect the wrong database or produce recommendations for the wrong environment. <br>
Mitigation: Confirm the target database and scope before running performance snapshots, reports, or index recommendation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-db-diagnose) <br>
- [Publisher profile](https://clawhub.ai/user/magicczc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON diagnostic output from dbskiter and should treat database details as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
