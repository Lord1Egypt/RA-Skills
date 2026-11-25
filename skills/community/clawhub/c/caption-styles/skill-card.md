## Description:

Provides 17 configurable animated caption styles and 52 presets for video, with guidance on timing, readable placement, contrast, and accessible plain-caption alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT

## Use Case:

Developers and video editors use this skill to choose a caption style and build timed, readable captions for short-form and other videos. It supports HyperFrames, Remotion, and ASS-based workflows; transcription and translation require separate tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the instructions may run HyperFrames without a pinned version.

Mitigation: Use a reviewed, fixed HyperFrames version before running its commands.

Risk: Security scan coverage is incomplete: one of 42 components was partly inspected and static analysis has limits.

Mitigation: Review the relevant files and dependencies before execution; treat the scan conclusion as limited by its stated coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/caption-styles)
- [Captioning references index](references/sources.md)
- [Netflix Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)
- [BBC Subtitle Guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)
- [WCAG 2.2 contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Remotion TikTok-style captions](https://www.remotion.dev/docs/captions/create-tiktok-style-captions)
- [HyperFrames caption components](https://github.com/heygen-com/hyperframes/tree/main/registry/components)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance]

**Output Format:** [Markdown guidance and JSON caption presets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preset values cover caption timing, typography, layout, and animation; use word-level timestamps for timed captions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
