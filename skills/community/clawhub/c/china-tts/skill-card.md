## Description: <br>
China Tts converts text to speech through the SiliconFlow API for China-accessible multilingual, dialect, emotion, podcast dialogue, and custom voice-cloning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to generate speech audio from text through SiliconFlow, including article narration, emotional reading, dialect speech, two-speaker podcast dialogue, and custom cloned voices. <br>

### Deployment Geography for Use: <br>
Global; optimized for users who need direct access from China. <br>

## Known Risks and Mitigations: <br>
Risk: Text and reference voice recordings are sent to SiliconFlow for cloud processing. <br>
Mitigation: Use the skill only for content you are permitted to send to the provider, and review SiliconFlow retention and deletion terms before uploading sensitive material. <br>
Risk: Voice cloning can create consent, impersonation, and privacy issues. <br>
Mitigation: Clone only voices you own or have explicit permission to use, protect custom voice IDs, and delete custom voices and generated audio when they are no longer needed. <br>
Risk: The skill requires a SiliconFlow API key. <br>
Mitigation: Store SILICONFLOW_API_KEY in the agent environment or secret store, avoid committing it to files, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ToBeWin/china-tts) <br>
- [Usage examples](references/examples.md) <br>
- [Voice list](references/voices.md) <br>
- [SiliconFlow speech API endpoint](https://api.siliconflow.cn/v1/audio/speech) <br>
- [SiliconFlow voice upload endpoint](https://api.siliconflow.cn/v1/uploads/audio/voice) <br>
- [SiliconFlow voice demos](https://soundcloud.com/siliconcloud/sets/siliconcloud-online-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown with curl commands, configuration guidance, and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SILICONFLOW_API_KEY; generated audio is saved under a workspace tts directory, typically as MP3.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
