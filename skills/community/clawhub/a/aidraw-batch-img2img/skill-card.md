## Description:

AIDraw批量图生图 automates Tencent Hunyuan AI batch img2img workflows by uploading reference images, applying custom prompts, generating multiple variants, and saving the resulting images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chottomattekimkim-droid](https://clawhub.ai/user/chottomattekimkim-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to batch-process local reference images through timiai.woa.com, generate multiple image variants with reusable prompt templates, and download the results to an organized folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Corporate or sensitive source images may be uploaded to timiai.woa.com during batch generation.

Mitigation: Run the skill only in a trusted environment and avoid confidential source folders unless upload is authorized.

Risk: The automation uses saved browser session cookies and copies them into direct image download requests.

Mitigation: Use a dedicated timiai browser profile or account, and constrain downloads to trusted timiai image hosts before relying on the script.

Risk: The server security verdict is suspicious due to unsafe, under-scoped cookie handling.

Mitigation: Review the script and security guidance before installation, especially for corporate workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chottomattekimkim-droid/skills/aidraw-batch-img2img)
- [Tencent Hunyuan AI image generation](https://timiai.woa.com/image-generation)
- [Keyword templates](references/keyword-templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands and a Python automation script that produces local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as PNG files using source-name and sequence-number filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
