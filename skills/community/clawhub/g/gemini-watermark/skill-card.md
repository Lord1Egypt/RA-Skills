## Description: <br>
Removes visible Gemini AI star or sparkle watermarks from images using reverse alpha blending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h1bomb](https://clawhub.ai/user/h1bomb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to run local image-cleanup commands against Gemini-generated images, including single-image and batch directory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's main purpose is removing visible AI watermarks, which can affect attribution, disclosure, or platform-rule expectations. <br>
Mitigation: Use it only on images the operator is authorized to edit, preserve originals, and check applicable disclosure or platform requirements before publishing edited outputs. <br>
Risk: Forced watermark removal can modify images that do not contain the expected visible Gemini watermark. <br>
Mitigation: Prefer detection mode, review outputs before use, and reserve force mode for images where the operator has confirmed the watermark location and size. <br>
Risk: The tool depends on locally installed Python packages. <br>
Mitigation: Install Pillow and numpy in an isolated virtual environment from trusted package sources. <br>


## Reference(s): <br>
- [Gemini Watermark Removal Algorithm](references/algorithm.md) <br>
- [Removing Gemini AI Watermarks: A Deep Dive into Reverse Alpha Blending](https://allenkuo.medium.com/removing-gemini-ai-watermarks-a-deep-dive-into-reverse-alpha-blending-bbbd83af2a3f) <br>
- [GeminiWatermarkTool C++ Reference Implementation](https://github.com/allenk/GeminiWatermarkTool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and local image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes JPEG, PNG, WebP, and BMP inputs; single-image runs write one cleaned image and directory runs write cleaned files to an output directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata, skill frontmatter, and script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
