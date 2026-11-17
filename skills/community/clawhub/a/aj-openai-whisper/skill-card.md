## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceundefeated](https://clawhub.ai/user/aceundefeated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to produce Whisper CLI guidance and commands for local audio transcription or translation without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running the Whisper CLI through Homebrew, which can add local binaries and dependencies.

Mitigation: Install from trusted Homebrew sources and confirm the whisper binary path before use.

Risk: Private recordings and generated transcript files may be exposed if audio paths or output directories are chosen carelessly.

Mitigation: Review audio file paths and output directories before running transcription commands, especially for sensitive recordings.

Risk: Whisper models are downloaded and cached locally on first use.

Mitigation: Ensure local model cache locations are acceptable for the deployment environment before first run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aceundefeated/skills/aj-openai-whisper)
- [OpenAI Whisper research page](https://openai.com/research/whisper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local transcription or translation commands using the whisper CLI; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
