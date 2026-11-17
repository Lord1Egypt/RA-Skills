## Description:

Analyze Bilibili AI-generated videos to extract/reverse-engineer prompts for imitation and replication, including frames, subtitles, ComfyUI/Seedance-format keyframe prompts, and scene breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jilanfang](https://clawhub.ai/user/jilanfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to analyze Bilibili AI-generated videos they are permitted to inspect, extract frames and subtitles, and produce prompt material for generating similar videos. It is intended for prompt reverse-engineering workflows that need keyframe prompts, scene sequencing, a master prompt, and voiceover reference text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and analyzes Bilibili videos, which can create copyright, permission, or misuse concerns when applied to content the user does not own or have permission to analyze.

Mitigation: Use it only on videos the user owns or is authorized to inspect, and review generated prompts before using them to imitate another creator's work.

Risk: Playlist URLs may cause yt-dlp to fetch more than one video.

Mitigation: Review Bilibili URLs before download and avoid playlist URLs unless multi-video download is intended.

Risk: Untrusted or excessive FPS values can cause unexpectedly large frame outputs or slow analysis.

Mitigation: Keep FPS low, use the documented 1 FPS default for short videos, and validate FPS values before running extraction.

Risk: Hard subtitle OCR is not implemented, so videos without embedded subtitle streams may produce an empty subtitle output.

Mitigation: Check whether the source video has embedded subtitles and treat empty subtitle files as a known limitation rather than complete transcript evidence.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/jilanfang/skills/bilibili-video-prompt-analyzer)
- [ClawHub publisher profile](https://clawhub.ai/user/jilanfang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with shell command examples, extracted text files, JPEG frame files, and comma-separated prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes technical metadata, 2-3 keyframe prompts, scene sequence breakdown, a full master prompt, a negative prompt when applicable, and extracted subtitle text.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
