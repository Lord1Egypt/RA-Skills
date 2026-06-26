## Description: <br>
Queue and publish local skills to ClawHub with a strict 5-per-hour cap using the local clawhub CLI and host scheduler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to queue local skill directories for ClawHub publishing while enforcing a five-attempts-per-hour limit. It helps coordinate local CLI publishing, status tracking, and scheduler-based execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queue-controlled command execution can run broader local shell commands than needed for publishing. <br>
Mitigation: Use dry-run first, avoid queue items with custom command fields, and prefer a fixed clawhub publish argument list before scheduling. <br>
Risk: Scheduled execution can repeatedly publish with the wrong account or configuration. <br>
Mitigation: Verify the logged-in ClawHub account and audit the helper before enabling cron or systemd scheduling. <br>


## Reference(s): <br>
- [ClawHub project homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update queue, state, and log files when the local helper is executed by the user or scheduler.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
