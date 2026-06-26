## Description: <br>
Converts scripts or copy into high-fidelity voice audio with selectable voices, emotion controls, SSML guidance, and post-processing for MP3 or WAV delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and production teams use this skill to turn written content into narration, podcast audio, advertisements, audiobooks, or other voice assets using available TTS providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires paid-service credentials and its instructions include a command that can print API keys. <br>
Mitigation: Use presence-only credential checks and never echo or log API key values. <br>
Risk: Text submitted for synthesis may be sent to ElevenLabs or OpenAI, and generated audio files are written locally. <br>
Mitigation: Use only text suitable for those providers and review local output paths before sharing or storing generated audio. <br>
Risk: Voice cloning or use of another person's voice can create consent and authorization concerns. <br>
Mitigation: Use cloned or third-party voices only when the user confirms they have the necessary rights and authorization. <br>


## Reference(s): <br>
- [Voice style guide](references/voice-style-guide.md) <br>
- [SSML guide](references/ssml-guide.md) <br>
- [Audio processing guide](references/audio-processing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated MP3 or WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated and post-processed audio files locally; uses external TTS providers when API keys are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
