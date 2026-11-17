## Description:

Cleans videos and screen recordings by guiding fixed-overlay removal, mask generation, frame extraction, optional Gemini-based frame repair, and video rebuilding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyuuuliu](https://clawhub.ai/user/hyuuuliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video editors, and agent operators use this skill to remove visible overlays from videos or screen recordings with deterministic FFmpeg paths first and targeted frame-repair workflows when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini mode sends video frames and masks to Google for model-based image editing.

Mitigation: Use Gemini mode only when external provider processing is intended, and confirm GEMINI_API_KEY configuration before running it.

Risk: Custom frame-edit mode can execute an operator-provided editor command once per frame.

Mitigation: Use only trusted editor commands and review command templates before processing video frames.

Risk: The reported security guidance warns that work-directory cleanup can create data-loss risk when pointed at an existing or valuable directory.

Mitigation: Use a new disposable work directory or keep cleanup behavior contained before passing --workdir.

Risk: Generated repairs are plausible visual cleanups rather than guaranteed recovery of covered content.

Mitigation: Review output for realism, temporal consistency, and residual artifacts before redistribution or downstream use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hyuuuliu/skills/cleanup-video-overlay)
- [Publisher profile](https://clawhub.ai/user/hyuuuliu)
- [Skill homepage](https://github.com/hyuuuliu/video-overlay-cleanup-skill)
- [Pipeline](references/pipeline.md)
- [Mask Strategies](references/mask-strategies.md)
- [Gemini Provider](references/gemini-provider.md)
- [Provider Integration](references/provider-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON manifests, generated masks, restored frames, and rebuilt video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require GEMINI_API_KEY for Gemini mode and can report frame count, estimated spend, token usage, and cleanup caveats.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
