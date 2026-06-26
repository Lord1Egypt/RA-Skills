## Description: <br>
Compress or convert generated images for delivery, preview, and social upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compress or convert local image files for delivery, preview, social upload, and lower file size. It supports single images, directories, recursive processing, WebP/PNG/JPEG targets, quality settings, and optional JSON summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes undisclosed image-generation code that can use APIs, credentials, network calls, and persistent configuration. <br>
Mitigation: Treat the release as a Review install, avoid scripts under scripts/vendor for compression-only use, and do not provide API keys or network access unless the publisher explains the bundled files or ships a compression-only version. <br>
Risk: The advertised compression workflow depends on local compressor tools and may fail or fall back depending on what is installed. <br>
Mitigation: Run the readiness check before use and install or select one of the supported local tools: sips, cwebp, or ImageMagick. <br>


## Reference(s): <br>
- [Tool Selection Notes](references/tool-selection.md) <br>
- [ClawHub skill page](https://clawhub.ai/632657122/compress-image) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files, json] <br>
**Output Format:** [Markdown guidance with shell commands; compressed image files; optional JSON CLI summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local compressors when available; WebP output requires cwebp or ImageMagick.] <br>

## Skill Version(s): <br>
9.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
