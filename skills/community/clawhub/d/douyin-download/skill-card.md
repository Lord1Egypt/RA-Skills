## Description:

Downloads watermark-free Douyin videos and extracts video transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whille](https://clawhub.ai/user/whille)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Douyin video metadata, download Douyin videos, and generate transcript Markdown from video audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin media is downloaded locally and audio is sent to SiliconFlow for transcription.

Mitigation: Use only non-sensitive videos with appropriate authorization, and remove local downloaded media and transcript outputs when no longer needed.

Risk: Transcript text may be sent to MiniMax when semantic segmentation is enabled.

Mitigation: Use --no-segment unless MiniMax processing is intended and approved for the transcript content.

Risk: URL fetching is broader than the Douyin-specific purpose requires.

Mitigation: Pass only trusted Douyin share links or modal IDs, and do not pass arbitrary non-Douyin URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whille/skills/douyin-download)
- [SiliconFlow API portal](https://cloud.siliconflow.cn/)
- [SiliconFlow audio transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, configuration]

**Output Format:** [Command-line output and Markdown transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and SILI_FLOW_API_KEY; MiniMax segmentation is optional and can be skipped with --no-segment.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
