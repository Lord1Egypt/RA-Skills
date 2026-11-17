## Description:

Converts text to speech and sends it to a specified Feishu user as an audio message when channel=feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangc](https://clawhub.ai/user/tangc)

### License/Terms of Use:


## Use Case:

Developers and workflow agents use this skill to produce audible Feishu notifications from text, especially when a voice message is preferred over a file or plain text message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text is sent through edge-tts and Feishu services.

Mitigation: Avoid sending secrets, regulated data, or sensitive personal content as voice-message text.

Risk: The skill uses Feishu app credentials from environment variables or local OpenClaw configuration.

Mitigation: Run it in an isolated environment with least-privilege Feishu credentials and avoid exposing credential-bearing logs or shell history.

Risk: The generated voice depends on a local edge-tts installation.

Mitigation: Use a pinned, reviewed edge-tts installation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangc/skills/feishu-send-voice)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, JSON]

**Output Format:** [Shell execution with JSON success or Feishu API error output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires text, a Feishu open_id, Feishu app credentials, ffmpeg, and edge-tts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
