## Description:

Transcribes Chinese audio to text with the Fun-ASR-Nano-2512 model, supporting one-shot CLI use and an optional local FastAPI service for repeated transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frozenarctic](https://clawhub.ai/user/frozenarctic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to transcribe Chinese or mixed Chinese-English audio files into text, especially for low-memory local workflows and domain vocabulary such as medical, insurance, and social security terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent API mode can keep a local transcription service and model process running after use.

Mitigation: Prefer the one-shot CLI mode for occasional files and stop the service when it is no longer needed.

Risk: The local path transcription endpoint can process arbitrary server-local file paths with weak safeguards.

Mitigation: Avoid exposing port 11890 and remove or tightly restrict the /transcribe/path endpoint before persistent use.

Risk: Startup scripts, dependencies, and model loading behavior require review before enabling persistent API mode.

Mitigation: Review the startup scripts and pin or verify dependencies and model artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frozenarctic/skills/funasr-nano-transcribe)
- [FunASR GitHub](https://github.com/alibaba-damo-academy/FunASR)
- [Model information](references/model_info.md)
- [Persistent usage guide](references/persistent_usage.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text transcripts, optional transcript files, JSON API responses, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can run as a one-shot CLI or as a persistent local service on port 11890.]

## Skill Version(s):

1.0.6 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
