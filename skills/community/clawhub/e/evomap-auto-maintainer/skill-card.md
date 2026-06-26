## Description: <br>
Maintains EvoMap node availability by checking status, sending heartbeat requests, and configuring recurring heartbeat automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanglingAI](https://clawhub.ai/user/zhanglingAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and EvoMap node operators use this skill to monitor node status and keep a configured node active through manual or scheduled heartbeat commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup command can add a recurring user-level cron task that continues sending EvoMap heartbeat requests. <br>
Mitigation: Review the crontab after setup and remove the heartbeat entry when the skill is no longer needed. <br>
Risk: EVOMAP_SECRET is used as a node credential for heartbeat requests. <br>
Mitigation: Treat EVOMAP_SECRET like a password and avoid exposing it in shared shell history, logs, or support messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanglingAI/evomap-auto-maintainer) <br>
- [EvoMap](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses EVOMAP_NODE_ID, EVOMAP_SECRET, and optional EVOMAP_LOG environment variables; setup can add a user-level cron heartbeat entry.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
