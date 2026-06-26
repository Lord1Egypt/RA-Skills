## Description: <br>
Check image DPI and intelligently upscale low-resolution images using super-resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and publishing teams use this skill to inspect image DPI, calculate print readiness, and upscale low-resolution images for print or document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation may pull unintended Python packages before the tool runs. <br>
Mitigation: Install only in a disposable virtual environment after cleaning and pinning requirements.txt to canonical packages such as pillow, numpy, opencv-python, and realesrgan. <br>
Risk: Batch processing can read many image files and write generated outputs across a folder tree. <br>
Mitigation: Run the tool against a specific input image folder and a dedicated output directory to avoid unintended bulk processing or overwrites. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/dpi-upscaler-checker) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON DPI reports, and generated image files from the local script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process a single image or recursively process supported image files in a folder; output may include JSON reports and upscaled image files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
