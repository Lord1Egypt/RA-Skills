## Description:

Transcribes recorded or live audio with OpenAI Whisper and can return transcripts, simple emotion labels, translations, and basic audio signal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to ask an agent to record or transcribe audio, translate speech, label simple emotions, and report basic signal features for meetings or audio analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recording or processing microphone audio can capture meetings, bystanders, or sensitive speech without adequate consent or retention controls.

Mitigation: Run recording commands only after all participants consent, use short durations, and confirm where WAV and transcript outputs are stored.

Risk: The skill depends on local audio and transcription packages that may change behavior across environments.

Mitigation: Install dependencies in a pinned, reviewed environment before using the skill with real audio.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create WAV and transcript outputs when recording or capture commands are run, depending on the local audio implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
