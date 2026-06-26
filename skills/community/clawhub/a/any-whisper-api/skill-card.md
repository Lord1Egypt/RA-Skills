## Description: <br>
Transcribe audio via API Whisper with any compatible local servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NW15D](https://clawhub.ai/user/NW15D) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users use this skill to transcribe local audio files through an OpenAI or Whisper-compatible transcription API, with options for model, language, prompt, output path, and JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio content and the bearer token are sent to the configured WHISPER_API_HOST. <br>
Mitigation: Use only a trusted local or known Whisper-compatible server, and avoid sensitive audio unless the endpoint's handling and retention are acceptable. <br>
Risk: The configured server address was flagged as unsafe to handle. <br>
Mitigation: Set WHISPER_API_HOST explicitly to a known endpoint and review the command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NW15D/any-whisper-api) <br>
- [OpenAI speech-to-text documentation](https://platform.openai.com/docs/guides/speech-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Transcript text or JSON written to a file by a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [By default, output is written beside the input audio file; callers can override the path with --out.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
