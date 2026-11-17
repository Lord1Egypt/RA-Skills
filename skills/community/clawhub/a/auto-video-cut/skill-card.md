## Description:

Automatically trims single-speaker videos by detecting silence and filler, scoring candidate segments, and producing rough-cut video outputs with reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and video-production teams use this skill to rough-cut single-speaker videos such as vlogs, tutorials, podcasts, and knowledge-sharing clips. It is not positioned for multi-person interviews or music-heavy/B-roll-heavy footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode can recursively delete the selected working directory.

Mitigation: Run only on copies of videos, use a dedicated empty working directory, and avoid passing any important folder as the third argument.

Risk: Generated transcripts and reports may contain private speech from source videos.

Mitigation: Treat transcripts and reports as sensitive and store or share them only where appropriate for the source content.

Risk: Dependency installation and media processing can affect the local environment.

Mitigation: Install dependencies in a virtual environment and review the skill before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/auto-video-cut)
- [FFmpeg download](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, generated video files, transcripts, and processing reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces clipped MP4 files and Markdown reports; batch mode can concatenate deduplicated clips.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
