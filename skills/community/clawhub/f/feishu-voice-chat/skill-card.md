## Description: <br>
Feishu Voice Chat handles Feishu voice messages by using Volcengine ASR to transcribe audio and Volcengine TTS to synthesize Feishu-compatible audio replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-neo](https://clawhub.ai/user/li-neo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to add Feishu voice conversation support, including speech-to-text for inbound audio and text-to-speech audio replies sent through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice content and synthesized reply text may be processed by Volcengine and sent through Feishu. <br>
Mitigation: Deploy only where users and administrators accept that data flow, and avoid sending sensitive or regulated audio unless the services are approved for that use. <br>
Risk: The Volcengine access token can authorize speech service usage if exposed. <br>
Mitigation: Store VOLC_ACCESS_TOKEN as a secret, restrict its scope to speech services where possible, and rotate it if exposure is suspected. <br>
Risk: Unpinned Python dependencies may change behavior across installations. <br>
Mitigation: Pin and review requests and python-dotenv versions before using the skill in sensitive or regulated environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/li-neo/feishu-voice-chat) <br>
- [Publisher profile](https://clawhub.ai/user/li-neo) <br>
- [Volcengine speech service console](https://console.volcengine.com/speech/app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON status objects, plain text transcripts, OGG audio files, and Feishu message command strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcengine speech credentials and Feishu/OpenClaw message integration; TTS output is written as OGG audio for Feishu voice messages.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
