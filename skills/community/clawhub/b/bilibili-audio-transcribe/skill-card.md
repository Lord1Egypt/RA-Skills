## Description:

Download audio from Bilibili or b23.tv links and transcribe it into txt, srt, and segment JSON with yt-dlp, ffmpeg, and faster-whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yizh4ng](https://clawhub.ai/user/yizh4ng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert Bilibili or b23.tv video links into local transcript, subtitle, and segment metadata files, especially for Chinese-language speech-to-text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads media from Bilibili or b23.tv and creates local transcript and media files.

Mitigation: Run it only on intended Bilibili or b23.tv URLs and choose an output directory appropriate for any sensitive transcript content.

Risk: The bootstrap workflow installs Python dependencies and troubleshooting may involve system package installation for ffmpeg.

Mitigation: Review or pin dependency versions before bootstrapping, and run system package-manager commands only when system-wide ffmpeg installation is intended.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/yizh4ng/skills/bilibili-audio-transcribe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated transcript files in txt, srt, and JSON formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local transcript text, SRT subtitles, and segment JSON under the selected output directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
