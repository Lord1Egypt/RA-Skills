## Description: <br>
Converts text to speech with Volcengine Doubao TTS, including voice, emotion, speed, volume, and pitch options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shandingdonren](https://clawhub.ai/user/shandingdonren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure Volcengine credentials and convert prompted text into spoken MP3 audio with selectable voices and playback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation and service credentials are sent to Volcengine/Bytedance. <br>
Mitigation: Use the skill only for text appropriate for that service, protect the access token as a secret, restrict config file permissions, and keep credentials out of repositories and backups. <br>
Risk: Broad read-aloud triggers could cause unintended TTS requests. <br>
Mitigation: Add confirmation or tighter command scoping before sending confidential or sensitive text to the external TTS API. <br>
Risk: Cloud TTS usage depends on network access, valid credentials, provider availability, and account billing limits. <br>
Mitigation: Verify token freshness and service entitlement before use, handle API failures explicitly, and monitor provider usage or quotas. <br>


## Reference(s): <br>
- [Volcengine](https://www.volcengine.com/) <br>
- [Volcengine Text-to-Speech Documentation](https://www.volcengine.com/docs/6561/97465) <br>
- [ClawHub Release Page](https://clawhub.ai/shandingdonren/doubao-tts-http) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration and bash snippets; generated audio is MP3.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Volcengine/Bytedance TTS API over HTTPS and save audio to /tmp or a user-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
