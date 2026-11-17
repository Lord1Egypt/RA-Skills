## Description:

Alibaba Cloud Bailian Qwen Image 2.0 image generation. Supports text-to-image and image-to-image (reference image + text). For product promotion image generation, e-commerce image editing, marketing material creation. Provides Python API, CLI tool, and ComfyUI custom nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[navygo](https://clawhub.ai/user/navygo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, e-commerce teams, and marketing teams use this skill to generate promotional images, edit product imagery, and integrate Alibaba Cloud Bailian Qwen Image 2.0 text-to-image or image-to-image workflows through Python, CLI, or ComfyUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles DashScope credentials and may attach the API key to an unvalidated image-download URL returned by the service.

Mitigation: Use a dedicated low-privilege DashScope API key with spending limits, validate image download hosts before sending Authorization headers, and avoid loading unrelated secrets from nearby .env files.

Risk: Prompts and reference images are sent to Alibaba Cloud for processing.

Mitigation: Do not submit sensitive prompts or images unless Alibaba Cloud processing is acceptable for the intended use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/navygo/skills/bailian-image-gen)
- [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com)
- [DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1)
- [ComfyUI workflow example](assets/comfyui_workflow.json)

## Skill Output:

**Output Type(s):** [image files, code, shell commands, configuration, guidance]

**Output Format:** [Generated image files plus Markdown guidance with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DASHSCOPE_API_KEY and network access to Alibaba Cloud DashScope services.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
