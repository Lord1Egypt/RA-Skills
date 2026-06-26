## Description: <br>
Local speech recognition using Alibaba DAMO Academy's FunASR for transcribing audio and video files with small-memory and large-model modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruitao](https://clawhub.ai/user/ruitao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files, video files, or trusted media URLs into text or JSON using local FunASR models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and process remote media URLs. <br>
Mitigation: Use trusted http/https URLs or local files, avoid private or internal URLs, and review URL handling before use in shared or sensitive networks. <br>


## Reference(s): <br>
- [FunASR installation guide](references/installation.md) <br>
- [Memory optimization guide](references/memory-optimization.md) <br>
- [Model comparison](references/model-comparison.md) <br>
- [Video transcription workflow](references/video-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/ruitao/funasr-asr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription output can include text or JSON metadata such as character count, segment count, duration, elapsed time, and selected model mode.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
