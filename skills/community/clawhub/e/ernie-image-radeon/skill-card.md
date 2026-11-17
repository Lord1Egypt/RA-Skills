## Description:

Ernie Image Radeon helps agents generate PNG images from Chinese or English text prompts using ERNIE-Image and ERNIE-Image-Turbo models via AMD Radeon Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwork4me](https://clawhub.ai/user/aiwork4me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to turn explicit image-generation requests into local image files with configurable model, size, batch count, seed, inference steps, guidance scale, and prompt enhancement options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default AMD Radeon Cloud endpoint uses HTTP, so prompts sent to it are not transport encrypted.

Mitigation: Use only non-sensitive prompts with the default endpoint, or configure a trusted HTTPS endpoint with `ERNIE_BASE_URL` before sending confidential or business-related prompts.

Risk: The optional URL response format downloads image data from provider-returned URLs.

Mitigation: Prefer the default `b64_json` response format unless the provider response path is trusted.

Risk: The documentation includes `curl | sh` installer guidance for `uv`, which can execute remote installer content directly.

Mitigation: Install `uv` through an approved package source or independently verify the installer before running it.

## Reference(s):

- [ERNIE-Image API Reference - AMD Radeon Cloud Edition](references/api-guide.md)
- [ClawHub skill page](https://clawhub.ai/aiwork4me/skills/ernie-image-radeon)
- [ernie-image-gen fork source page](https://clawhub.ai/aiwork4me/ernie-image-gen)

## Skill Output:

**Output Type(s):** [shell commands, files, json, guidance]

**Output Format:** [Markdown guidance with shell commands; generated output is PNG files, MEDIA paths, or optional JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ERNIE-Image and ERNIE-Image-Turbo, seven image sizes, batches of 1-4 images, seed control, 4-20 inference steps, guidance scale from 1.0-7.5, prompt enhancement, quiet mode, and custom output directories.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
