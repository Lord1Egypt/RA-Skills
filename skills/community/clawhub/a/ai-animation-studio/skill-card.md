## Description:

AI Animation Studio turns user stories into storyboarded AI animation videos with selectable visual styles, voiceover, subtitles, and background music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to convert story prompts into short animated videos, including scene breakdowns, image and video generation prompts, voice assignments, subtitle planning, BGM selection, and local MP4 composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External media-generation and TTS services may process submitted stories, private images, dialogue, or other sensitive creative inputs.

Mitigation: Avoid confidential stories, private images, personal dialogue, and unauthorized voice-like content unless the operator has permission to submit that material to the configured services.

Risk: The workflow depends on Windows-specific local paths and a hardcoded doubao-media script location.

Mitigation: Review and update local paths, resource directories, and the doubao-media script path before running the skill in a new environment.

Risk: The workflow invokes ffmpeg and local media files during video composition.

Mitigation: Run it in a controlled workspace and review input and output paths before processing media files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/systiger/skills/ai-animation-studio)
- [Skill Documentation](artifact/SKILL.md)
- [BGM Library](artifact/BGM_LIBRARY.md)
- [Volcengine ARK Console](https://console.volcengine.com/ark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, JSON production scripts, shell commands, and MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Doubao/ARK media generation, Edge TTS, ffmpeg, and local media resources; final videos are described as MP4 H.264/AAC with burned-in subtitles when synthesis succeeds.]

## Skill Version(s):

2.1.1 (source: server release metadata and artifact/SKILL.md changelog, released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
