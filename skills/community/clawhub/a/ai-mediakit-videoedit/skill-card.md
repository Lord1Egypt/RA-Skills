## Description: <br>
AI MediaKit Video Edit helps an agent analyze local videos with subtitles or danmaku, propose clip segments for a user's editing request, and synthesize edited video outputs with FFmpeg and optional Remotion text effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn local video, subtitle, and danmaku files into a reviewed clip plan, then generate edited videos with transitions and optional text overlays. It is useful for highlight extraction, topic-based video cuts, multi-clip splicing, and Bilibili-style danmaku-informed editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local video, subtitle, and danmaku files provided by the user. <br>
Mitigation: Use it only with files intended for processing and avoid providing unrelated sensitive media or text files. <br>
Risk: The generated edit plan can write or overwrite video output paths. <br>
Mitigation: Review the clip plan and choose an output path that can be safely overwritten before confirming execution. <br>
Risk: Optional text effects require installing and running the bundled Remotion template dependencies. <br>
Mitigation: Run npm install only inside the included template directory and use a trusted Remotion server if REMOTION_SERVE_URL is set. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volc-ai-mediakit/ai-mediakit-videoedit) <br>
- [Bilibili danmaku XML format reference](artifact/references/danmaku_format.md) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON clip/effects plans, shell commands, and generated local video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before running video synthesis; output paths are selected by the user or plan.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
