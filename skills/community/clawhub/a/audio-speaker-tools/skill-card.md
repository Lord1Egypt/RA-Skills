## Description: <br>
Speaker separation, voice comparison, and audio processing tools for multi-speaker audio, voice cloning, speaker verification, segment extraction, ElevenLabs sample preparation, and diarization validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmfinlan](https://clawhub.ai/user/cmfinlan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and audio engineers use this skill to separate speakers from recordings, compare voice samples, extract clean speaker segments, and prepare or evaluate samples for voice cloning and speaker verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process speaker identity, voice cloning, and speaker verification data without adequate consent or privacy safeguards. <br>
Mitigation: Use it only with audio the user is authorized to process and with consent from the speakers. <br>
Risk: Extracted speaker clips and comparison outputs can expose sensitive biometric information. <br>
Mitigation: Treat generated audio clips, diarization metadata, and similarity results as sensitive data and delete temporary files when no longer needed. <br>
Risk: Uploading samples to ElevenLabs or another third party can disclose voice data outside the local environment. <br>
Mitigation: Review the destination service and obtain appropriate consent before uploading voice samples. <br>
Risk: Voice cloning and speaker verification workflows can be misused for impersonation or surveillance. <br>
Mitigation: Avoid impersonation, surveillance, or authentication decisions without appropriate authorization and human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cmfinlan/audio-speaker-tools) <br>
- [ElevenLabs Instant Voice Cloning Best Practices](references/elevenlabs-cloning.md) <br>
- [Resemblyzer Voice Similarity Scoring Guide](references/scoring-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with bash commands, Python script outputs, JSON metadata, RTTM diarization files, JSONL segment records, and WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local virtual environments, separated speaker WAV files, diarization.rttm, segments.jsonl, meta.json, and voice comparison JSON when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
