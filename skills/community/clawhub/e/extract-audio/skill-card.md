## Description:

Extract audio from videos or recordings as MP3, M4A, WAV, or FLAC, trim or normalize it, prepare 16 kHz mono WAV for transcription, and export embedded subtitles as SRT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tariksucu](https://clawhub.ai/user/tariksucu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can follow this skill to extract or convert audio from video and recordings, prepare audio for transcription, and export supported text subtitles. It provides ffmpeg commands and Converter Studio options for common formats and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external Converter Studio or browser fallback may involve transferring sensitive media to an external conversion service.

Mitigation: Use local ffmpeg for sensitive media. Before using an external fallback, disclose the transfer and obtain consent.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/tariksucu/converter-studio/tree/main/skills/extract-audio)
- [Converter Studio](https://converter.studio)
- [ClawHub release page](https://clawhub.ai/tariksucu/skills/extract-audio)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Audio files, Subtitle files]

**Output Format:** [Markdown guidance with ffmpeg commands; resulting audio files (MP3, M4A, WAV, or FLAC) and subtitle files (SRT or VTT)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps the source file, names results after it, and reports duration, format, size, and selected track.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
