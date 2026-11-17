## Description:

Dub YouTube videos with Voice.ai TTS. Turn scripts into publish-ready voiceovers with chapters, captions, and audio replacement for YouTube long-form and Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmogremlin](https://clawhub.ai/user/gizmogremlin)

### License/Terms of Use:


## Use Case:

External creators and developers use this skill to turn YouTube scripts into Voice.ai narration, captions, chapters, review pages, and optional dubbed videos. It supports long-form videos, Shorts, course content, screen recordings, and batch voiceover production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends script text and API credentials to Voice.ai for text-to-speech generation.

Mitigation: Use only scripts suitable for Voice.ai processing, keep VOICE_AI_API_KEY scoped and rotatable, and review the destination endpoint before use.

Risk: Changing VOICEAI_API_BASE can redirect requests that include credentials or script content.

Mitigation: Set VOICEAI_API_BASE only to a trusted HTTPS Voice.ai endpoint.

Risk: Generated ffmpeg helper scripts can execute media-processing commands derived from local paths and files.

Mitigation: Inspect helper scripts before running them, especially when media paths or files came from someone else.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gizmogremlin/skills/dub-youtube-with-voiceai)
- [Voice.ai](https://voice.ai)
- [Voice.ai Dashboard](https://voice.ai/dashboard)
- [Voice.ai API Reference](references/VOICEAI_API.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with CLI commands; generated audio, video, caption, chapter, HTML review, manifest, and timeline files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+; ffmpeg is optional for stitching, MP3 encoding, loudness normalization, and video dubbing.]

## Skill Version(s):

0.1.6 (source: server release metadata; artifact frontmatter states 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
