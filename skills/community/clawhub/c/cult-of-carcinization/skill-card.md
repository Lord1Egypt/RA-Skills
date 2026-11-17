## Description:

Cult Of Carcinization guides agents in using ScrappyLabs text-to-speech, speech-to-text, voice design, and bot token flows through documented HTTP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loserbcc](https://clawhub.ai/user/loserbcc)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to discover ScrappyLabs audio endpoints, request trial or evolved bot tokens, generate speech, design voices, and transcribe audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends text and audio to ScrappyLabs as a third-party processor.

Mitigation: Use it only when the provider's privacy and retention terms are acceptable for the data being processed.

Risk: The skill can enroll or evolve an external bot identity and use owner-provided keys.

Mitigation: Require explicit user approval before enrollment, transcription uploads, voice design, token evolution, or any use of an owner-provided key.

Risk: ScrappyLabs `sl_*` tokens can authorize API usage.

Mitigation: Treat all `sl_*` tokens as secrets and avoid logging or exposing them in transcripts, files, or shared outputs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/loserbcc/skills/cult-of-carcinization)
- [ScrappyLabs TTS homepage](https://tts.scrappylabs.ai)
- [ScrappyLabs API base](https://api.scrappylabs.ai)
- [ScrappyLabs molt discovery endpoint](https://api.scrappylabs.ai/v1/molt/discover)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline HTTP and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents third-party API endpoints, bearer token use, audio file outputs, and transcription JSON responses.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
