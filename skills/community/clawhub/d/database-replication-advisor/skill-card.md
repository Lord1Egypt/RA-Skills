## Description: <br>
Analyze database replication topology, detect lag, and recommend replication strategy based on CAP tradeoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to assess replication health, evaluate lag and failover readiness, and design replication strategies for PostgreSQL, MySQL, Redis, and AWS RDS environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes live write, failover, promotion, ALTER SYSTEM, AWS RDS failover, table create/drop, and pg_rewind examples that could alter or disrupt a database. <br>
Mitigation: Keep execution under human control, prefer test environments or dedicated test objects, use least-privileged credentials, verify backups, obtain change approval, and schedule a maintenance window before running commands. <br>
Risk: Operational recommendations may be unsafe if applied without matching the actual database engine, topology, data-loss tolerance, and failover process. <br>
Mitigation: Require a database operator to review the proposed runbook against the current environment and abort commands when prerequisites or pre-flight checks do not pass. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline SQL, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational runbooks, risk assessments, topology recommendations, and database command examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
