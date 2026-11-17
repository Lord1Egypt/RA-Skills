## Description:

Generate images with FLUX models via the inference.sh CLI, including text-to-image, image-to-image, and LoRA-based custom style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate and adapt FLUX images through inference.sh commands for product imagery, art, style transfer, and image-to-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends mutable remote installer and unpinned package commands that can execute code outside the reviewed artifact.

Mitigation: Review commands before running them, pin package sources where possible, and verify installer checksums before installing the CLI.

Risk: Remote image-generation workflows can expose sensitive prompts, private image URLs, or sensitive media to the inference service.

Mitigation: Use non-sensitive prompts and media, avoid secrets or private URLs, and follow the service's data handling requirements before submitting inputs.

## Reference(s):

- [Flux Image on ClawHub](https://clawhub.ai/okaris/skills/flux-image)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Image Generation Example](https://inference.sh/docs/examples/image-generation)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote inference commands and image URL inputs.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
