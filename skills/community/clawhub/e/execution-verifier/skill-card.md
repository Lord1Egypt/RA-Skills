## Description: <br>
Enforce real progress for long-running tasks by separating execution from reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RichardSun700](https://clawhub.ai/user/RichardSun700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to require evidence-backed progress reports for long-running agent tasks, verify recent file or commit activity, and trigger a configured executor when no progress is detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Closed-loop mode can automatically run caller-supplied local shell commands and recurring cron work. <br>
Mitigation: Restrict commands to a specific project, avoid unattended --force cron runs, and require human approval before any command that can change files, agent state, scheduled jobs, or external services. <br>
Risk: Progress checks based on file timestamps and git commits can miss useful work that does not change artifacts or can overcount timestamp-only changes. <br>
Mitigation: Pair verifier output with task-specific tests, diffs, or reviewed artifacts before treating a progress report as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RichardSun700/execution-verifier) <br>
- [Publisher profile](https://clawhub.ai/user/RichardSun700) <br>
- [Verifier progress script](scripts/verify_progress.py) <br>
- [Closed-loop verifier script](scripts/verify_execute_verify.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; verifier scripts output JSON status objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress checks rely on local file timestamps, git commits, STATUS.md, OPEN_TASKS.md, and configured verify and execute commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
