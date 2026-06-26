## Description: <br>
Speech recognition CLI for AI agent automation. Transcribe audio from stdin, files, or URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dionren](https://clawhub.ai/user/dionren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe recorded, streamed, or piped audio into text, JSON, SRT, or VTT output. It supports local ASR engines and optional cloud transcription engines for automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs or runs a downloaded speech recognition executable. <br>
Mitigation: Verify the release source and checksum before trusting the binary, and run installation in an environment appropriate for downloaded tools. <br>
Risk: Audio supplied to transcription may contain private or sensitive speech. <br>
Mitigation: Use local engines for private audio when possible, and review provider privacy terms before sending audio to cloud engines. <br>
Risk: Optional cloud engines require API keys for OpenAI, Doubao, or Deepgram. <br>
Mitigation: Protect API keys, avoid exposing them in prompts or logs, and use scoped or dedicated keys where available. <br>
Risk: Service-style engines can keep local transcription services running after use. <br>
Mitigation: Check engine status and stop service engines when transcription work is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dionren/asr-claw) <br>
- [Project Homepage](https://github.com/llm-net/asr-claw) <br>
- [Release Binary Download](https://github.com/llm-net/asr-claw/releases/latest/download/asr-claw-${os}-${arch}) <br>
- [Release Checksums](https://github.com/llm-net/asr-claw/releases/latest/download/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output may be JSON, plain text, SRT, or VTT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transcription segments, full text, selected engine, audio duration, and timing metadata.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
