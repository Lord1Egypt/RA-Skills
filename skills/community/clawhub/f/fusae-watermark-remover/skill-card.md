## Description: <br>
Automatically detects and removes watermarks from images using AI-powered inpainting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fusae](https://clawhub.ai/user/fusae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-processing users use this skill to process image files or directories when they need to detect corner watermarks, preview masks, and produce cleaned image copies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external watermark-remover package and a model that may be downloaded at runtime. <br>
Mitigation: Install only from trusted sources and verify the package and model source before use. <br>
Risk: Removing watermarks can modify images in ways that may be inappropriate without permission. <br>
Mitigation: Use the skill only on images you have the right to modify. <br>
Risk: Directory processing can affect many images in one run. <br>
Mitigation: Run preview mode or test on copies before processing directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fusae/fusae-watermark-remover) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Image files and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-image and directory processing, mask preview output, detection sensitivity options, and OpenCV fallback.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
