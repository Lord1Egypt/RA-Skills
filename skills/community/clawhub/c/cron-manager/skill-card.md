## Description: <br>
Manage, schedule, monitor, and report on recurring cron tasks with flexible patterns, dependencies, priorities, timezones, and execution logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to create, inspect, pause, resume, manually run, and monitor recurring local tasks through a JSON-emitting command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and run local shell commands. <br>
Mitigation: Review every command before adding or running it, restrict who can create tasks, and periodically inspect persisted task files and logs. <br>
Risk: Task definitions and execution logs may contain sensitive command text, output, or errors. <br>
Mitigation: Avoid putting secrets in task commands or command output, secure the cron data directory, and review retained logs. <br>


## Reference(s): <br>
- [Cron Manager on ClawHub](https://clawhub.ai/indigas/cron-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task definitions and execution logs in local JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
