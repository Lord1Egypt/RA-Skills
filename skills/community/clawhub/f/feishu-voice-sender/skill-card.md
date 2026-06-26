## Description: <br>
Feishu Voice Sender converts provided text to speech with Edge TTS, converts the audio to Feishu-compatible OPUS format, and sends it to a Feishu chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwek](https://clawhub.ai/user/wwek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send spoken Feishu notifications, reminders, status updates, or alerts from text. It supports reply-style sending to the current chat and explicit target chat delivery when a target is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text provided to the skill is sent to Microsoft Edge TTS for speech generation. <br>
Mitigation: Do not provide secrets, regulated data, or sensitive business content unless that use is approved. <br>
Risk: Generated audio is posted into a Feishu chat using existing OpenClaw permissions. <br>
Mitigation: Verify the target chat before sending and limit use to chats where the content is appropriate. <br>
Risk: The skill depends on Python packages and FFmpeg installed in the runtime environment. <br>
Mitigation: Install dependencies in a virtual environment where possible and keep system packages maintained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwek/feishu-voice-sender) <br>
- [Publisher profile](https://clawhub.ai/user/wwek) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Command-line status text and generated OPUS audio file sent through Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, edge-tts, FFmpeg, OpenClaw, and existing Feishu send permissions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
