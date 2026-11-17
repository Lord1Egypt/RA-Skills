## Description:

Smart Audio Analyzer transcribes audio, labels speakers with persistent voice profiles, detects recording scenes, and generates structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jojowillwater](https://clawhub.ai/user/jojowillwater)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze recordings such as meetings, interviews, talks, and rowing training sessions. It produces transcripts, speaker labels, scene-specific summaries, and follow-up notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be sent to AssemblyAI, Gemini, or OpenRouter when those API keys are configured.

Mitigation: Use local Whisper for offline transcription when cloud upload is not acceptable, and process only recordings whose privacy terms permit external ASR.

Risk: The authoritative security review reports a command-injection flaw in the Whisper fallback path for untrusted or oddly named audio files.

Mitigation: Avoid the Whisper fallback for untrusted filenames until the invocation is fixed; use trusted paths, sanitized filenames, or a configured cloud ASR engine.

Risk: Generated transcripts, raw JSON, summaries, and voice-db.json can contain sensitive audio content, speaker metadata, or biometric voice embeddings.

Mitigation: Store outputs in access-controlled locations, tighten file permissions when needed, and delete transcripts, summaries, raw JSON, or voice-db.json after use.

Risk: The authoritative security review reports weak biometric-data controls around stored speaker embeddings.

Mitigation: Require explicit speaker confirmation before profile updates and document retention or deletion expectations for voiceprint data.

## Reference(s):

- [Smart Audio Analyzer ClawHub page](https://clawhub.ai/jojowillwater/skills/audio-analyzer)
- [Voice profiles reference](references/voice-profiles.md)
- [General scene template](references/scenes/general.md)
- [Meeting scene template](references/scenes/meeting.md)
- [Interview scene template](references/scenes/interview.md)
- [Talk scene template](references/scenes/talk.md)
- [Rowing scene template](references/scenes/rowing.md)
- [WeSpeaker releases](https://github.com/wenet-e2e/wespeaker/releases)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Text transcripts, JSON metadata, and Markdown summaries with setup and execution commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript, raw JSON, and optional summary files beside the analyzed audio; optional voiceprint tooling can update local voice profile data.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter says 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
