## Description: <br>
A local-first recurring task scheduler for agents that supports daily, weekly, monthly, and interval schedules with task lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation-focused users can use this skill to define local recurring tasks, inspect upcoming runs, pause or resume jobs, archive jobs, and review run history. It is intended for local scheduling workflows where task definitions and execution history remain on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled task text may cause the agent to perform unintended future actions during later sessions. <br>
Mitigation: Review every scheduled task before activation and keep task text precise, especially for deletion, backups, account changes, or external notifications. <br>
Risk: Local schedule and run-history files can persist tasks beyond the session in which they were created. <br>
Mitigation: Inspect the local jobs and runs files regularly, and pause or archive stale tasks that should no longer run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-scheduler-pro-free) <br>
- [Detailed reference](artifact/references/detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks plus local JSON task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local scheduler files under ~/workspace/scheduler/cron/ when the agent executes the provided examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
