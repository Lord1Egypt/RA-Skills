## Description: <br>
Converts text into speech with Edge TTS and sends the resulting voice message to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwek](https://clawhub.ai/user/wwek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn short notification text into Chinese voice messages and send them to Feishu chats for reminders, status updates, and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or regulated text can be processed by Edge TTS and delivered to Feishu as audio. <br>
Mitigation: Do not submit passwords, tokens, regulated data, or confidential incident details unless that use is approved for both Edge TTS processing and Feishu delivery. <br>
Risk: A generated voice message can be sent to the wrong Feishu chat if the target or current chat is incorrect. <br>
Mitigation: Confirm the target chat before sending, especially when using proactive delivery with an explicit target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwek/feishu-tts-edge) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Audio files, Feishu messages, Guidance] <br>
**Output Format:** [Command-line execution that generates an OPUS audio file and sends a Feishu voice message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, edge-tts, FFmpeg, OpenClaw Feishu channel access, and a target or current chat.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
