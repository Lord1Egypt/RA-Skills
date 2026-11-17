## Description:

Downloads watermark-free Douyin videos and extracts speech transcripts with optional semantic segmentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whille](https://clawhub.ai/user/whille)

### License/Terms of Use:


## Use Case:

Developers and content workflows use this skill to inspect Douyin video information, download video media, and extract speech transcripts. It can write transcript Markdown and optionally segment transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript and audio content may be sent to external transcription or segmentation services.

Mitigation: Use only media appropriate for those services, and pass --no-segment or remove MINIMAX_API_KEY when MiniMax transcript segmentation is not wanted.

Risk: The skill accepts broad network targets and downloads media from resolved URLs.

Mitigation: Run it in a constrained network environment and use an output directory you control.

Risk: The skill writes downloaded media, audio intermediates, and transcript Markdown files.

Mitigation: Review generated files before sharing and avoid using shared or sensitive output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whille/skills/douyin-download-v2)
- [SiliconFlow Cloud](https://cloud.siliconflow.cn/)
- [SiliconFlow transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [CLI text output and Markdown transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and SILI_FLOW_API_KEY for transcription; MINIMAX_API_KEY enables optional semantic segmentation.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
