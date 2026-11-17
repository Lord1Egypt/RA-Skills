## Description:

Windows-oriented Douyin video download and transcript extraction skill that parses share links, downloads watermark-free videos, transcribes audio with local Whisper base, and can optionally segment transcript text.

This skill is for research and development only.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows command-line users use this skill to inspect Douyin video metadata, download videos, and extract Chinese-language transcript markdown from video audio. It is positioned for personal learning and research use, with optional semantic segmentation when users choose to provide the required MiniMax API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default transcript segmentation can send full transcript text to a third-party MiniMax API when MINIMAX_API_KEY is available.

Mitigation: Use --no-segment for private, business, customer, or regulated speech unless sending transcript text to MiniMax is acceptable.

Risk: The workflow depends on locally installed command-line tools and Python Whisper packages.

Mitigation: Install Whisper and related dependencies in an isolated, non-admin environment with pinned package versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/douyindownloadwhisper)
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Console text and Markdown transcript files produced through command-line workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download video files, create temporary audio files, and save transcript.md under the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
