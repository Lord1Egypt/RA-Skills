## Description: <br>
Proactive cron job health monitoring, failure detection, and auto-repair delegation for recurring and silent cron failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygq19901001](https://clawhub.ai/user/ygq19901001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect cron job health, diagnose recurring or silent failures, and prepare repair or delegation steps for cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to change, run, create, or disable cron jobs and write files while attempting repairs. <br>
Mitigation: Require explicit approval for cron updates, runs, creation, disable actions, shell commands, and file writes; restrict repairs to known job IDs and approved directories. <br>
Risk: A generated repair payload could misdiagnose a cron failure or change an operational schedule unexpectedly. <br>
Mitigation: Review generated repair cron payloads before execution and verify changes with a bounded test run before relying on the repair. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/biobrain-cron-health-monitor) <br>
- [Server-resolved GitHub source](https://github.com/Ygq19901001/biobrain-cron-health-monitor) <br>
- [Common cron error catalog](references/common-errors.md) <br>
- [Cron repair playbook](references/repair-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with cron command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cron updates, test runs, repair payloads, shell commands, and file writes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
