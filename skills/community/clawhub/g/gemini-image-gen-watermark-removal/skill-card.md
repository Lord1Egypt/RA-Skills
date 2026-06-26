## Description: <br>
Guides an agent through using a logged-in Google Gemini web session to generate and download images, then optionally remove Gemini watermarks with GeminiWatermarkTool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imkingjh999](https://clawhub.ai/user/imkingjh999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Google Gemini web image generation, download generated images, and optionally remove watermarks before sharing or further processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to control a logged-in Google browser session for Gemini. <br>
Mitigation: Install and run it only when browser automation for that account is intended, and review agent actions before prompts, downloads, or account-affecting steps. <br>
Risk: Watermark removal can alter image provenance and may be inappropriate for images the user is not authorized to modify. <br>
Mitigation: Use watermark removal only on images the user is authorized to modify, and retain the original generated image when provenance needs to be preserved. <br>
Risk: The optional Feishu sharing snippet includes a hard-coded recipient path and sends images and captions to an external service. <br>
Mitigation: Do not run the sharing snippet unless the recipient is replaced and confirmed and the user accepts sending the image and caption to Feishu. <br>
Risk: The workflow depends on installing or using GeminiWatermarkTool, a third-party binary or package. <br>
Mitigation: Verify the GeminiWatermarkTool source and release before installation or execution. <br>


## Reference(s): <br>
- [Google Gemini](https://gemini.google.com) <br>
- [GeminiWatermarkTool](https://github.com/allenk/GeminiWatermarkTool) <br>
- [GeminiWatermarkTool Releases](https://github.com/allenk/GeminiWatermarkTool/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with browser-tool examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Google browser session, OpenClaw Browser Tool access, and optional third-party watermark-removal tooling.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
