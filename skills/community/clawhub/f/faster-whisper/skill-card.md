## Description:

Local speech-to-text using faster-whisper. 4-6x faster than OpenAI Whisper with identical accuracy; GPU acceleration enables ~20x realtime transcription. SRT/VTT/TTML/CSV subtitles, speaker diarization, URL/YouTube input, batch processing with ETA, transcript search, chapter detection, per-file language map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theplasmak](https://clawhub.ai/user/theplasmak)

### License/Terms of Use:


## Use Case:

Developers, engineers, and external users use this skill to run local speech-to-text workflows for audio, video, podcasts, subtitles, speaker diarization, transcript search, translation, and batch transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary network media and contact external media sites.

Mitigation: Use only trusted URLs and avoid private RSS feeds or sensitive media URLs unless the execution environment is isolated.

Risk: Diarization and model access can involve Hugging Face credentials.

Mitigation: Prefer cached credentials, avoid passing tokens directly on the command line, and restrict token scope and filesystem access.

Risk: Setup and update paths can install or upgrade unpinned dependencies and optional Docker images.

Mitigation: Review dependencies before installation, pin versions where required, and run setup in a controlled environment.

Risk: Generated HTML transcripts from untrusted audio may carry content-handling risk.

Mitigation: Sanitize generated HTML before opening or sharing it when the source media is untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theplasmak/skills/faster-whisper)
- [Declared skill homepage](https://github.com/ThePlasmak/faster-whisper)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [Distil-Whisper paper](https://arxiv.org/abs/2311.00430)
- [SYSTRAN faster-whisper models](https://huggingface.co/collections/Systran/faster-whisper)
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated transcript, subtitle, JSON, CSV, HTML, or statistics files depending on requested flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be streamed to the user for short text results or written to files for subtitles, structured data, HTML, multi-format exports, and batch workflows.]

## Skill Version(s):

1.5.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
