## Description:

Generates and edits images locally with Fooocus (Stable Diffusion XL), including text-to-image, image variations, upscaling, inpainting, outpainting, face swap, and style transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wszhhx](https://clawhub.ai/user/wszhhx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to set up and operate local Fooocus image generation workflows without relying on cloud image APIs. It helps agents choose prompts, styles, presets, API calls, and shell commands for local generation and image-editing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install software, clone remote code, modify files under the user's home directory, and start a local Fooocus service.

Mitigation: Review the installer before use, install into a verified directory, avoid --force unless the target path is confirmed, and keep the service bound to localhost.

Risk: Prompts or selected images may be sent to a configured API endpoint if the user points the skill at a non-local Fooocus service.

Mitigation: Use local endpoints for sensitive prompts or personal images, and only use remote endpoints after explicitly accepting that data transfer.

Risk: The scanner verdict is suspicious because the installer and runtime guidance create host-safety and privacy concerns.

Mitigation: Review and scan the skill before deployment, then monitor generated commands and configuration changes before execution.

## Reference(s):

- [Fooocus Gradio API Reference](artifact/references/fooocus_api.md)
- [Fooocus Parameters Guide](artifact/references/parameters_guide.md)
- [Fooocus Presets](artifact/references/presets.md)
- [Fooocus GitHub](https://github.com/lllyasviel/Fooocus)
- [Fooocus Wiki](https://github.com/lllyasviel/Fooocus/wiki)
- [Fooocus Troubleshoot Guide](https://github.com/lllyasviel/Fooocus/blob/main/troubleshoot.md)
- [Hugging Face Fooocus Models](https://huggingface.co/lllyasviel)
- [SDXL Prompt Guide](https://stable-diffusion-art.com/sdxl-prompt/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, API parameters, and generated local image file paths when generation succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a local Fooocus service, Python dependencies, model downloads, GPU resources, and optional user-selected input images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
