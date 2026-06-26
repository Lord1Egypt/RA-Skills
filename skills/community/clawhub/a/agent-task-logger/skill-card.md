## Description: <br>
Agent Task Logger helps agents initialize a workspace log and record task starts, command execution, status updates, and errors in a Tomcat-style local log file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gerald-luo](https://clawhub.ai/user/gerald-luo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to keep a real-time local task log for agent work, including command history, task outcomes, timing, and errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command text, error messages, private paths, or other sensitive details may be saved in workspace log files. <br>
Mitigation: Keep logs in a trusted workspace, restrict access where appropriate, and avoid logging API keys, passwords, customer data, private paths, or other secrets. <br>
Risk: Long-running use can accumulate local log data that no longer needs to be retained. <br>
Mitigation: Rotate, archive, or delete old log files according to the workspace's retention needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gerald-luo/agent-task-logger) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local log-file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes task events to a workspace log file such as logs/agent-task.log.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
