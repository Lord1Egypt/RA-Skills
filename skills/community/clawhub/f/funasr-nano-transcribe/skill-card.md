## Description: <br>
Uses the Fun-ASR-Nano-2512 lightweight speech recognition model to transcribe Chinese audio through CLI scripts or a local FastAPI service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frozenarctic](https://clawhub.ai/user/frozenarctic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe Chinese audio files, including domain-specific medical, insurance, and social security terminology, either one file at a time or through a reusable local transcription service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a long-running local ASR service that continues using memory after transcription. <br>
Mitigation: Prefer CLI transcription for one-off or sensitive audio, and stop the service when finished. <br>
Risk: The local /transcribe/path endpoint can process host files by path if the service is running. <br>
Mitigation: Keep the service bound to localhost and use /transcribe/path only for files explicitly selected for transcription. <br>
Risk: The model source and dependency versions affect trustworthiness in sensitive environments. <br>
Mitigation: Review the bundled model source and dependency versions before deployment in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frozenarctic/funasr-nano-transcribe) <br>
- [FunASR GitHub](https://github.com/alibaba-damo-academy/FunASR) <br>
- [Model information](references/model_info.md) <br>
- [Persistent usage guide](references/persistent_usage.md) <br>
- [Quickstart guide](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcriptions, Markdown guidance with shell commands, and JSON API responses from the local service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-file CLI transcription, batch transcription, and a localhost FastAPI service for repeated use.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
