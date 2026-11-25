## Description:

Autonomous timeline AI video editor for TikTok, Reels, YouTube Shorts, and podcasts. Use when editing videos from natural language or canonical actions: smart jump cuts, silence removal, 9:16 active-speaker reframing, 216 animated captions and subtitles, B-roll cutaways, After Effects motion graphics, VFX keying, color grading, voiceover, audio cleanup, and cloud MP4 export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors, content creators, and developers can use an agent to plan and execute timeline edits for short-form social videos and podcasts, inspect rendered previews, and export finished video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because four local path-like references could not be resolved, leaving some content outside the scan's coverage.

Mitigation: Review the unresolved references and the corresponding source before installation; treat the clean verdict as medium-confidence evidence.

Risk: The editing workflow sends source media to a cloud video editing service and requires a service account and API key.

Mitigation: Use only media approved for cloud processing, and provide the API key through the editing tool's configuration rather than in prompts or shared content.

## Reference(s):

- [Levea video editing service](https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=ai-agentic-video-editor)
- [Levea API](https://api.livecore.ai)
- [ClawHub skill release](https://clawhub.ai/brajendrak00068/skills/ai-agentic-video-editor)

## Skill Output:

**Output Type(s):** [Text, JSON, Video URL]

**Output Format:** [Structured edit status and verification report with project identifiers and an MP4 download URL when export completes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The exported video is rendered by the Levea service; completion may be synchronous or queued.]

## Skill Version(s):

1.0.36 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
