## Description:

Generates images with SiliconFlow using Kolors, FLUX, and Qwen-Image models when the user provides a SiliconFlow API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duyiliu](https://clawhub.ai/user/duyiliu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate images from text prompts through the SiliconFlow image generation API. It is useful when an agent needs to propose the required API call, configuration, or shell command for creating a PNG image file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to SiliconFlow under the user's API key.

Mitigation: Do not include secrets, proprietary text, or personal data in prompts, and use the skill only when SiliconFlow API use is acceptable.

Risk: The bundled script defaults to saving output under /tmp when no output path is supplied.

Mitigation: Provide an explicit output path for generated images and avoid running the script with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duyiliu/skills/gen-image)
- [SiliconFlow homepage](https://siliconflow.cn)
- [SiliconFlow cloud console](https://cloud.siliconflow.cn)
- [SiliconFlow image generations endpoint](https://api.siliconflow.cn/v1/images/generations)
- [SiliconFlow models endpoint](https://api.siliconflow.cn/v1/models)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples; the bundled script emits status text and saves a PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SILICONFLOW_API_KEY; accepts a text prompt, optional output path, MODEL, and SIZE.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
