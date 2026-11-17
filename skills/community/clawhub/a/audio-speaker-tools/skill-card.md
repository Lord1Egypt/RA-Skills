## Description:

Speaker separation, voice comparison, and audio processing tools for multi-speaker audio, voice cloning, speaker verification, segment extraction, sample preparation, and diarization validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmfinlan](https://clawhub.ai/user/cmfinlan)

### License/Terms of Use:


## Use Case:

Developers and audio engineers use this skill to separate speakers from recordings, compare voice samples, prepare voice-cloning samples, and validate diarization or speaker-similarity results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning and speaker verification can be used on voices without proper authorization.

Mitigation: Use the skill only with voices the user is authorized to process, clone, or compare.

Risk: Audio samples, separated speaker files, and similarity scores can expose sensitive biometric information.

Mitigation: Handle generated audio and score outputs as sensitive data with appropriate storage, sharing, and retention controls.

Risk: Some workflows involve uploading audio or using gated third-party services.

Mitigation: Review ElevenLabs and Hugging Face privacy and retention terms before uploading audio or running service-backed workflows.

Risk: Speaker similarity scores may be overused as an authentication decision.

Mitigation: Do not use score thresholds as the sole basis for real authentication or access-control decisions.

Risk: Hugging Face credentials may be exposed if passed through command-line arguments.

Mitigation: Pass credentials through protected environment variables such as HF_TOKEN and avoid the --token argument in shared shells or logs.

Risk: The setup script installs unpinned Python dependencies.

Mitigation: Run setup in an unprivileged environment and review or pin dependencies before production use.

## Reference(s):

- [ElevenLabs Instant Voice Cloning Best Practices](references/elevenlabs-cloning.md)
- [Resemblyzer Voice Similarity Scoring Guide](references/scoring-guide.md)
- [ClawHub release page](https://clawhub.ai/cmfinlan/skills/audio-speaker-tools)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, Python script usage, JSON metadata, JSONL segments, RTTM diarization output, and WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce per-speaker WAV files, diarization.rttm, segments.jsonl, meta.json, plain-text similarity scores, JSON similarity reports, and pass/fail exit codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
