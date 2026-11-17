## Description:

A local Chinese-language video editing skill that uses moviepy and ffmpeg to trim, merge, resize, caption, add text or music, adjust speed, extract or replace audio, and generate text-only explainer videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncsimok](https://clawhub.ai/user/ncsimok)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to prepare short-form Chinese-language video assets locally, including clips for Douyin or Xiaohongshu. It is suited for common editing tasks such as trimming, merging, subtitles, background music, resizing, speed changes, and audio replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that accept explicit output paths may overwrite existing local media files.

Mitigation: Check output filenames before execution and write generated media to a working copy or dedicated output directory.

Risk: Local media processing can modify or extract content from user-supplied files.

Mitigation: Use trusted input files and review generated video, audio, and subtitle outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncsimok/skills/doorstep-video-editor)
- [Publisher profile](https://clawhub.ai/user/ncsimok)

## Skill Output:

**Output Type(s):** [shell commands, guidance, files, JSON]

**Output Format:** [Markdown guidance with bash commands; the helper script emits JSON status and local video or audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with user-provided media files and writes edited media outputs to the selected output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
