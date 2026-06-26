## Description: <br>
Automates batch image-to-image generation on Tencent Hunyuan AI by uploading reference images, applying prompt keywords, generating multiple variants, and saving downloaded results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chottomattekimkim-droid](https://clawhub.ai/user/chottomattekimkim-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to automate Windows batch processing of reference images on timiai.woa.com, generate multiple prompt-guided variants, and download named PNG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script saves browser login state and cookies for timiai.woa.com in a persistent local browser profile. <br>
Mitigation: Run it only on a trusted machine and clear the saved browser profile after use if the session should not be retained. <br>
Risk: Reference images are uploaded to timiai.woa.com during generation. <br>
Mitigation: Use only images the user is authorized to upload and avoid sensitive or restricted content unless policy permits. <br>
Risk: Hardcoded source folder, prompt text, and generation count can cause unintended uploads or excessive generation runs. <br>
Mitigation: Review and edit these configuration values before each run. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chottomattekimkim-droid/aidraw-batch-img2img) <br>
- [Tencent Hunyuan AI image generation](https://timiai.woa.com/image-generation) <br>
- [Keyword templates](references/keyword-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The automation script downloads generated images as PNG files named from the source image and sequence number.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
