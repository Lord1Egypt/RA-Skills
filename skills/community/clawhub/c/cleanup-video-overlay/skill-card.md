## Description: <br>
Use this skill when the user wants to clean a video or screen recording by removing overlays such as status bars, notification banners, floating controls, subtitle bars, fixed watermarks, or other surface UI elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyuuuliu](https://clawhub.ai/user/hyuuuliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and content operators use this skill to remove visible overlays from videos or screen recordings, choose an FFmpeg or Gemini-based cleanup path, generate masks, and rebuild cleaned video outputs with caveats about reconstruction quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gemini mode uploads selected video frames and masks to Google Gemini. <br>
Mitigation: Use the local FFmpeg removelogo path for sensitive recordings, and only enable Gemini mode when the user accepts provider upload and API-key use. <br>
Risk: Custom frame-editor commands can execute arbitrary local commands during per-frame restoration. <br>
Mitigation: Use trusted editor commands only, inspect command templates before execution, and keep the edit scope limited to required input, mask, output, and frame-index placeholders. <br>
Risk: Output and work directories may be overwritten or cleaned up during video processing. <br>
Mitigation: Choose explicit output and work directories, avoid pointing them at valuable source folders, and preserve the work directory when intermediate frames or masks need review. <br>
Risk: Covered video regions are plausible visual reconstructions, not guaranteed factual recovery of hidden content. <br>
Mitigation: Keep masks tight, prefer deterministic FFmpeg cleanup for stable overlays, and label generative results as visual cleanup when reviewing or publishing outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hyuuuliu/cleanup-video-overlay) <br>
- [Pipeline](references/pipeline.md) <br>
- [Mask Strategies](references/mask-strategies.md) <br>
- [Gemini Provider](references/gemini-provider.md) <br>
- [Provider Integration](references/provider-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and references to generated video and work-directory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce masks, frame folders, run manifests, usage summaries, rebuilt videos, and caveats about visual reconstruction quality.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
