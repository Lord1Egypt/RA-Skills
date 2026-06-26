## Description: <br>
Database scheduling tool that guides agents through dbskiter backup, scheduled task, execution log, scheduler daemon, and DAG workflow commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to direct an agent through database backups, scheduled job management, execution log review, scheduler daemon control, and DAG workflow execution with dbskiter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage database backups, scheduled jobs, workflows, and scheduler daemons, which can affect data availability and recurring automation. <br>
Mitigation: Before execution, require confirmation of the database, task or workflow name, schedule, command, expected impact, and stop or removal procedure. <br>
Risk: Broad scheduler control without explicit scoping could apply changes to the wrong database or automation target. <br>
Mitigation: Constrain use to the intended database and review task, workflow, and daemon commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-db-scheduler) <br>
- [Publisher profile](https://clawhub.ai/user/magicczc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and short status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require an explicit database name and may create, enable, disable, run, or remove recurring database automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
