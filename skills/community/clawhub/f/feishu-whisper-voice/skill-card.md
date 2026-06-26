## Description: <br>
Uses Faster-Whisper speech recognition with Feishu TTS to transcribe voice messages and support two-way voice replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15071664](https://clawhub.ai/user/15071664) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to transcribe voice or audio messages with Faster-Whisper and generate text or voice replies through Feishu TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files, transcripts, and local caches can contain sensitive voice content. <br>
Mitigation: Install only where the Feishu bot or authorized user should access voice messages, and delete local transcript files or caches after processing sensitive audio. <br>
Risk: Runtime package installation or untrusted package mirrors can introduce dependency risk. <br>
Mitigation: Use an isolated virtual environment and preinstall pinned dependencies from trusted sources before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/15071664/feishu-whisper-voice) <br>
- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper) <br>
- [HuggingFace Faster-Whisper Base Model](https://huggingface.co/systran/faster-whisper-base) <br>
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; helper scripts produce terminal text and transcript files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process local audio files, write local transcript files, and use cached speech recognition models.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
