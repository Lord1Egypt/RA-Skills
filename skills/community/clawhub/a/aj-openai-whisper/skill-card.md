## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceundefeated](https://clawhub.ai/user/aceundefeated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local speech-to-text or translation jobs with the Whisper CLI, choosing model size and output format for audio files without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the Homebrew `openai-whisper` package and first-use model downloads introduce local dependencies and cached model files. <br>
Mitigation: Install only in an approved environment and confirm the package, model cache location, and available disk space before use. <br>
Risk: Audio files and generated transcripts may contain sensitive content. <br>
Mitigation: Review input paths and output directories before running Whisper, and store transcripts only in approved locations. <br>
Risk: Model size choices trade speed for accuracy, which can affect transcript quality. <br>
Mitigation: Choose a model appropriate for the use case and review important transcripts before relying on them. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub Skill Page](https://clawhub.ai/aceundefeated/aj-openai-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local audio file paths, output directories, Whisper task selection, model selection, and generated transcript or subtitle files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
