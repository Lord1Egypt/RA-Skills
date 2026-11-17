## Description:

Generate images with DrawThings through an Automatic1111-compatible Stable Diffusion API for text prompts, image workflows, and batch generation on Mac with MLX/CoreML acceleration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dustinparsons](https://clawhub.ai/user/dustinparsons)

### License/Terms of Use:


## Use Case:

Developers and creative users use this skill to generate PNG images from text prompts through a configured DrawThings API, including variations, batch generation, presets, and reproducible seeded outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to the configured DrawThings endpoint, which may be remote if DRAWTHINGS_URL is changed.

Mitigation: Keep DRAWTHINGS_URL on localhost unless the remote server is intentionally trusted, and avoid private or secret data in prompts.

Risk: Generated PNG files and sidecar JSON can include prompt and generation metadata.

Mitigation: Strip metadata before sharing generated files when privacy matters.

Risk: Community model files can create supply-chain risk.

Mitigation: Prefer verified .safetensors models from trusted sources over untrusted checkpoint files.

## Reference(s):

- [DrawThings API Reference](references/api-reference.md)
- [Recommended Models for DrawThings](references/models.md)
- [CivitAI model repository](https://civitai.com)
- [Hugging Face model hub](https://huggingface.co/models)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; the script writes PNG files and optional JSON metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DRAWTHINGS_URL or defaults to localhost; generated files may include prompt and generation metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
