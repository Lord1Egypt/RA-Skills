## Description:

Monitor F5-TTS distributed training on the 9-GPU mining rig (Local-LLM) without interfering with the process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pbseiya](https://clawhub.ai/user/pbseiya)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check GPU utilization, training log progress, and system load for an F5-TTS distributed training run over SSH while avoiding disruption to the running process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to connect by SSH to the Local-LLM host and inspect a live training process.

Mitigation: Confirm the target host and run only the listed monitoring commands so the active training process is not interrupted.

Risk: The skill asks the agent to update HEARTBEAT.md status files after probing training status.

Mitigation: Update status only in a known local project path and avoid modifying training data, checkpoints, or remote environment files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pbseiya/skills/f5tts-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes monitoring commands and local status-update guidance; does not produce code or configuration files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
