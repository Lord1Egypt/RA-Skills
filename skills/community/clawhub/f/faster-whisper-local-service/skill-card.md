## Description: <br>
Faster Whisper Local Service provisions a local OpenClaw speech-to-text backend using faster-whisper, exposed as a localhost HTTP service for voice transcription workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neldar](https://clawhub.ai/user/neldar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a local speech-to-text backend for browser, Telegram, and other voice input workflows without relying on recurring external transcription APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service installs Python dependencies, downloads Whisper model weights, and runs as a persistent user service. <br>
Mitigation: Review the documented install paths, confirm local disk and memory capacity, and use the documented systemd commands to stop, disable, or remove the service when it is no longer needed. <br>
Risk: Audio uploads are decoded by GStreamer, which processes binary media input. <br>
Mitigation: Keep GStreamer and Python dependencies updated from trusted package sources, and preserve the documented upload-size, audio-signature, and localhost binding controls. <br>
Risk: The first model startup requires network access and stores model files locally. <br>
Mitigation: Plan for the initial Hugging Face model download or pre-download models for restricted environments; after caching, the service can run locally without recurring external transcription API calls. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [faster-whisper model download documentation](https://github.com/SYSTRAN/faster-whisper#model-download) <br>
- [ClawHub release page](https://clawhub.ai/neldar/faster-whisper-local-service) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and deployable shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local HTTP transcription service, a Python virtual environment, and a user-level systemd service when deployed.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
