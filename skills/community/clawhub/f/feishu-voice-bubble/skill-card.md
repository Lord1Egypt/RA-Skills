## Description: <br>
Send native voice bubble messages in Feishu/Lark chats by converting text to Opus audio with Microsoft Edge TTS for Feishu audio message delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SAOKiritoKun](https://clawhub.ai/user/SAOKiritoKun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu/Lark bot operators use this skill to turn text into native voice-bubble audio messages, including long text split into multiple Opus files when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for voice generation may leave the user's machine for Microsoft Edge TTS processing. <br>
Mitigation: Do not use the skill for secrets, credentials, private personal data, or regulated business content unless that external processing is acceptable. <br>
Risk: Generated voice audio may be uploaded to Feishu/Lark when sent as a voice bubble. <br>
Mitigation: Review the text and intended chat destination before sending generated audio. <br>
Risk: The skill depends on an internet-hosted TTS service and has no stated service-level guarantee. <br>
Mitigation: Confirm network access and availability before relying on it for time-sensitive messaging workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SAOKiritoKun/feishu-voice-bubble) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates .opus audio files for Feishu/Lark voice bubbles; long text can be split into numbered output files.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
