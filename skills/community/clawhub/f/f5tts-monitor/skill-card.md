## Description: <br>
Monitor F5-TTS distributed training on the 9-GPU mining rig (Local-LLM) without interfering with the process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pbseiya](https://clawhub.ai/user/pbseiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to monitor F5-TTS distributed training status on a specific remote GPU rig without changing the running training process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to SSH into a named remote machine. <br>
Mitigation: Install only when that host and account are expected, and confirm SSH target details before use. <br>
Risk: Heartbeat updates may expose more training log detail than needed. <br>
Mitigation: Review HEARTBEAT.md updates and keep status notes limited to necessary progress, temperature, and ETA information. <br>
Risk: Monitoring commands could disrupt training if changed into write or process-control actions. <br>
Mitigation: Keep execution to the listed read-only commands and avoid modifying data, checkpoints, environments, or running processes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pbseiya/f5tts-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only monitoring posture; heartbeat updates should avoid unnecessary sensitive log details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
