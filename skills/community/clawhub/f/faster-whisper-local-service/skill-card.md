## Description:

Provisions a localhost OpenClaw speech-to-text service using faster-whisper for local voice transcription workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neldar](https://clawhub.ai/user/neldar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install and manage a local OpenClaw speech-to-text backend for browser, Telegram, and other voice workflows without recurring external transcription API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deploy script creates and enables a persistent systemd user service on the local machine.

Mitigation: Review environment variables before deployment and use the documented systemctl stop, disable, and daemon-reload commands to remove the service when it is no longer needed.

Risk: Initial setup installs Python dependencies and downloads faster-whisper model weights from Hugging Face.

Mitigation: Install only in environments where dependency installation and model download are acceptable, and plan for the documented disk and memory requirements.

Risk: Audio conversion depends on GStreamer media parsers processing uploaded binary data.

Mitigation: Keep GStreamer packages updated from trusted OS repositories and retain the documented upload-size, magic-byte, localhost binding, and CORS restrictions.

## Reference(s):

- [Faster Whisper Model Download Documentation](https://github.com/SYSTRAN/faster-whisper#model-download)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/neldar/skills/faster-whisper-local-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with bash commands and generated local service files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, verification, and service-management guidance for a local HTTP transcription service.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
