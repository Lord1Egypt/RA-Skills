## Description:

Audio Tools helps agents extract WAV audio from video, clip audio, play media, transcribe speech with Whisper, and extract audio or video metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[risehorizon](https://clawhub.ai/user/risehorizon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to automate common local media workflows, including audio extraction, audio clipping, playback, transcription, and metadata inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routine use may install or upgrade Python packages in the active environment.

Mitigation: Use an isolated virtual environment and preinstall reviewed, pinned dependencies before running the skill.

Risk: Playback or transcription of untrusted or sensitive media may expose local data or process malicious media inputs.

Mitigation: Avoid elevated privileges, confirm the media source before playback or transcription, and handle sensitive files in a controlled workspace.

Risk: Security evidence reports an unsafe metadata parser that needs review before installation.

Mitigation: Review metadata extraction behavior before deployment and avoid processing untrusted media for metadata until review is complete.

## Reference(s):

- [Audio Tools Usage](references/usage.md)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [Python Downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text or Markdown guidance with inline shell commands; generated outputs may include WAV audio, JSON metadata, JSON transcription, and TXT transcription files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription output includes text, language, duration, timestamps, average log probability, and no-speech probability when Whisper is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
