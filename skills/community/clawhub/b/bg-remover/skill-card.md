## Description: <br>
Remove, replace, or blur image backgrounds using AI-powered segmentation with rembg and U2-Net. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jxhgzs](https://clawhub.ai/user/jxhgzs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-editing users can use this skill to run local commands that remove image backgrounds, replace them with a color or image, or blur backgrounds for portrait-style output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation adds Python packages and the first model run downloads the U2-Net segmentation model. <br>
Mitigation: Install in an environment where package and model downloads are acceptable; use a virtual environment when possible. <br>
Risk: The tool reads user-provided image paths and writes processed PNG files to default or requested output paths. <br>
Mitigation: Process only images intended for the tool and choose output paths deliberately before running commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs PNG files with default suffixes or a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
