## Description: <br>
Cross-Session Task Manager provides file-based task indexes and progress templates that help agents resume ongoing work across sessions, channels, or threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imchongliu](https://clawhub.ai/user/imchongliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add a simple persistent task-memory workflow to an agent workspace, using active-task, closed-task, and per-project progress files to continue work after a session ends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task files may retain sensitive project details longer than intended. <br>
Mitigation: Do not store secrets, credentials, customer data, or sensitive personal details in task files, and periodically review or delete old progress files. <br>
Risk: Agents may continue using persistent task memory after the user no longer wants it. <br>
Mitigation: Remove the AGENTS.md or HEARTBEAT.md rules and archive or delete the task files when persistent task memory is no longer desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imchongliu/cross-session-tasks) <br>
- [Publisher Profile](https://clawhub.ai/user/imchongliu) <br>
- [ACTIVE-TASKS Template](artifact/templates/ACTIVE-TASKS.md) <br>
- [CLOSED-TASKS Template](artifact/templates/CLOSED-TASKS.md) <br>
- [Progress Template](artifact/templates/progress.md) <br>
- [Example Progress File](artifact/examples/example-progress.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local task-state files; users control what information is stored.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
