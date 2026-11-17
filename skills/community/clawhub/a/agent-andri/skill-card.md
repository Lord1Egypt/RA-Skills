## Description:

Agent Andri periodically sends its status report to the meeting-room by appending a message to a designated local file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alibabacloudservice19-collab](https://clawhub.ai/user/alibabacloudservice19-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run Andri as a worker agent that reports idle status into a shared meeting-room coordination file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script writes visible status messages into a local meeting-room coordination file.

Mitigation: Run it only in a workspace where this coordination file is expected and appropriate.

Risk: The status loop runs continuously until externally stopped.

Mitigation: Run it under supervision or with external lifecycle controls.

Risk: The skill documents NV_API_KEY even though the current script does not use it.

Mitigation: Avoid providing NV_API_KEY unless a future version requires it and handles it as a secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alibabacloudservice19-collab/skills/agent-andri)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text status messages appended by a shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a timestamped idle-status line every 30 seconds to the configured meeting-room file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
