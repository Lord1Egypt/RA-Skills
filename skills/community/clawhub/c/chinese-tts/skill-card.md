## Description: <br>
Generate Chinese TTS audio and send as Feishu voice message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Waao666](https://clawhub.ai/user/Waao666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn Chinese text into Opus voice audio suitable for Feishu voice messages. It is intended for requests to generate, read aloud, or send Chinese voice/audio content through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent through the workflow may be processed by Microsoft Edge TTS and carried through Feishu. <br>
Mitigation: Avoid secrets, credentials, regulated data, and confidential business text unless those external services are approved for the content. <br>
Risk: Voice messages can be sent to an unintended Feishu recipient. <br>
Mitigation: Confirm the Feishu recipient before sending generated audio. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Waao666/chinese-tts) <br>
- [Publisher Profile](https://clawhub.ai/user/Waao666) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates Opus audio files for Feishu voice-message upload when the required local tools and workspace paths are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
