## Description: <br>
Guided voice cloning workflow from recording tips to first playback, including audio quality checks, SenseAudio platform guidance, and preview generation with a cloned voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to prepare a voice recording, check recording quality, complete cloning on the SenseAudio platform, and generate an initial preview from the resulting voice_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive voice recordings and preview requests may be sent to SenseAudio without an explicit consent and privacy checkpoint. <br>
Mitigation: Add a clear consent step before any upload, explain that audio may be sent to SenseAudio, and proceed only for voices the user owns or has clear permission to clone. <br>
Risk: Voice cloning can be misused for impersonation or unauthorized voice reproduction. <br>
Mitigation: Use the workflow only for the user's own voice or a voice with documented permission, and decline requests that lack clear authorization. <br>
Risk: A SenseAudio API key is required for automated checks and preview generation. <br>
Mitigation: Use a dedicated, revocable API key and avoid sharing it in prompts, logs, or generated files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scikkk/clone-wizard) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and plain-language diagnostic feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY plus curl, jq, and xxd; may generate a local MP3 preview file from SenseAudio TTS output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
