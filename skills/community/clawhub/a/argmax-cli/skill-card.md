## Description: <br>
On-device speech-to-text with Whisper and text-to-speech with Qwen3-TTS using the whisperkit-cli command-line tool on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZachNagengast](https://clawhub.ai/user/ZachNagengast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe user-provided audio files into text and generate spoken audio replies with a local macOS CLI. It is suited for voice-message workflows where models are downloaded once and inference then runs on-device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Homebrew formula and first-run Hugging Face model downloads introduce external supply-chain dependencies. <br>
Mitigation: Install only trusted formulae and prefetch or verify required models before use in restricted, offline, or production environments. <br>
Risk: The optional local API server exposes transcription and translation endpoints on localhost when started. <br>
Mitigation: Start the server only for workflows that intentionally need the endpoint, bind it to localhost, and stop it when the workflow is complete. <br>


## Reference(s): <br>
- [WhisperKit documentation and model list](https://github.com/argmaxinc/WhisperKit) <br>
- [ClawHub release page](https://clawhub.ai/ZachNagengast/argmax-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks; runtime CLI outputs text transcripts and audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS and the whisperkit-cli binary; models may download on first run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
