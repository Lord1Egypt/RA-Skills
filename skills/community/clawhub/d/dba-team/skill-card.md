## Description: <br>
DBA多AI协作系统 coordinates database expert personas for architecture design, daily operations, troubleshooting, performance tuning, migration, security, reporting, and training across Oracle, MySQL, PostgreSQL, SQL Server, Chinese domestic databases, MongoDB, Redis, and ClickHouse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pc-study](https://clawhub.ai/user/pc-study) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators, developers, and operations teams use this skill to route database requests to specialized DBA personas and produce structured plans, diagnostics, reports, migration guidance, optimization advice, and final recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to automatically save DBA environment details, task history, and user preferences, which can retain sensitive operational context. <br>
Mitigation: Disable memory or review and delete stored memory before sharing passwords, connection strings, hostnames, production topology, or incident details. <br>
Risk: Scheduled inspections, reports, and backup validation workflows could act on production databases without sufficient review or privileges control. <br>
Mitigation: Require explicit approval for automated workflows and use least-privilege, task-specific database access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pc-study/dba-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured sections for requirements, task planning, execution process, and final solution.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
