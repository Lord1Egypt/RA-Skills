## Description: <br>
Generates educational and demo videos programmatically using Remotion, React, reusable layout components, text-to-speech narration, subtitles, and visual composition guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to scaffold and guide Remotion-based tutorial, explainer, and demo videos with scene layouts, subtitle workflows, rendering scripts, and troubleshooting references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example patterns may execute project content dynamically during local video generation. <br>
Mitigation: Replace dynamic Function-based resolution with a strict parser or allowlist before using the patterns with untrusted project content. <br>
Risk: Rendering guidance may weaken browser safety controls or inject MathJax/SVG output into a rendering pipeline. <br>
Mitigation: Avoid disabled Chromium web security for untrusted content and sanitize MathJax or SVG output before rendering. <br>
Risk: Process cleanup examples can terminate the wrong local process if process IDs or patterns are not checked. <br>
Mitigation: Verify process IDs and command patterns before running pkill, kill, or kill -9 cleanup commands. <br>
Risk: Unreviewed npm dependencies can affect local rendering and subtitle generation workflows. <br>
Mitigation: Pin or review npm dependencies before installation and use this skill as a trusted local development helper. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linhongbijkm-dot/edu-video-generator) <br>
- [Setup guide](references/setup.md) <br>
- [Remotion component templates](references/templates.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Remotion documentation](https://www.remotion.dev/docs) <br>
- [Lucide icons](https://lucide.dev/icons) <br>
- [edge-tts](https://github.com/rany2/edge-tts) <br>
- [Noto fonts](https://fonts.google.com/noto) <br>
- [KaTeX supported functions](https://katex.org/docs/supported.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, JavaScript, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local project files, Remotion components, subtitle files, rendering commands, and video workflow configuration.] <br>

## Skill Version(s): <br>
4.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
