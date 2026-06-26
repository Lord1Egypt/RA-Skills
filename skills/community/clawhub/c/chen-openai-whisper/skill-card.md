## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and other external users use this skill to run local speech-to-text or translation with the Whisper CLI and produce transcript or subtitle files without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation and execution of a local CLI that may download model files. <br>
Mitigation: Install only if you are comfortable using Homebrew to install Whisper and allowing Whisper to download local model files. <br>
Risk: Transcription commands process user-selected audio and write transcript or subtitle files. <br>
Mitigation: Transcribe only audio you intend to process and choose an output directory where transcript files are expected. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline Whisper CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write transcript or subtitle files to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
