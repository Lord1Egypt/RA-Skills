## Description: <br>
Local voice system for OpenClaw using faster-whisper for inbound transcription and Edge TTS for outbound replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenredmond-straiteis](https://clawhub.ai/user/stephenredmond-straiteis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add voice-message transcription and spoken replies to OpenClaw workflows. It supports local faster-whisper transcription, Edge TTS reply generation, cached outbound audio, installation scripts, and voice configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation claims the workflow is fully offline and private, while the server security summary says hosted Edge TTS behavior conflicts with those claims. <br>
Mitigation: Treat outbound TTS text as potentially sent to the TTS provider, avoid sensitive content, or replace hosted Edge TTS with a local TTS engine before using it for private workflows. <br>
Risk: Installer and runtime scripts install unpinned Python packages and system packages, copy executable files, and run local subprocesses. <br>
Mitigation: Review scripts before installation, run them in a constrained environment, pin dependencies where possible, and require explicit operator approval for system package installation. <br>
Risk: Audio filenames and text inputs flow into local subprocess paths and command strings. <br>
Mitigation: Use trusted file paths, avoid untrusted filenames, and prefer safer subprocess argument handling before exposing the workflow to arbitrary user uploads. <br>
Risk: Generated speech is cached locally and may retain sensitive response content. <br>
Mitigation: Configure cache cleanup, restrict filesystem access to the cache directory, and avoid generating audio for sensitive text unless retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephenredmond-straiteis/edge-tts-voice-system) <br>
- [Voice Models Reference](references/voice_models.md) <br>
- [Piper voices model artifact](https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx) <br>
- [Piper voices model metadata](https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; runtime scripts emit transcribed text, JSON-like text, and generated audio file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses faster-whisper for speech-to-text, Edge TTS for hosted text-to-speech, ffmpeg for audio conversion, and local caching for generated reply audio.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
