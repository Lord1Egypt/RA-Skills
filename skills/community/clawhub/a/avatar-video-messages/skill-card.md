## Description:

Generate and send video messages with a lip-syncing VRM avatar. Use when user asks for video message, avatar video, video reply, or when TTS should be delivered as video instead of audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thewulf7](https://clawhub.ai/user/thewulf7)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to turn text or audio into lip-synced avatar video messages and send them as Telegram video notes. It is suited for conversational agents that need a video reply instead of an audio-only response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports inconsistent npm package identity in the installer.

Mitigation: Review the npm package identity before installing and prefer a pinned, verified package.

Risk: Generated audio or video content and configured avatar or background assets may be sent through Telegram.

Mitigation: Use the skill only when that sharing behavior is intended and the selected assets are appropriate to transmit.

Risk: The artifact includes an overbroad temporary-file cleanup command.

Mitigation: Replace wildcard cleanup with deletion of the exact output file for the current run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thewulf7/skills/avatar-video-messages)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell and tool-command examples; generated runtime artifact is an MP4 video message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented workflow sends the generated MP4 as a Telegram video note and then returns NO_REPLY.]

## Skill Version(s):

0.1.2 (source: server evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
