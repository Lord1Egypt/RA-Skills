## Description:

Creates videos from text by generating a storyboard, image sequence, voiceover, and ffmpeg-based MP4 assembly guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, educators, and developers use this skill to turn a topic or script into short-form or presentation-style videos with generated images, narration, and MP4 composition steps.

### Deployment Geography for Use:

Global; documentation emphasizes users who need services reachable from mainland China.

## Known Risks and Mitigations:

Risk: The skill depends on mutable third-party skills for image generation and text-to-speech.

Mitigation: Verify or pin china-image-gen and china-tts before granting them workspace or credential access.

Risk: The skill requires a SiliconFlow API key and references persistent environment configuration.

Mitigation: Use a dedicated low-quota key, avoid storing it permanently unless the file is locked down, and rotate the key if it may have been exposed.

## Reference(s):

- [china-video-gen Skill Page](https://clawhub.ai/tobewin/skills/china-video-gen)
- [Dependencies Reference](references/dependencies.md)
- [ffmpeg Composition Reference](references/ffmpeg.md)
- [Storyboard Reference](references/storyboard.md)
- [ffmpeg Downloads](https://ffmpeg.org/download.html)
- [china-image-gen Skill](https://clawhub.ai/ToBeWin/china-image-gen)
- [china-tts Skill](https://clawhub.ai/ToBeWin/china-tts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with storyboard text, prompts, ffmpeg commands, and workspace file paths for generated media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of frames, voiceover audio, concat files, and a final MP4 in the user's workspace.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
