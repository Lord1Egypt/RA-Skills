## Description:

Generate AI images with FLUX, Gemini, Grok, Seedream, Reve, and 50+ models via the inference.sh CLI for text-to-image, image-to-image, inpainting, LoRA, image editing, upscaling, and text rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers, creators, and external users use this skill to select and run inference.sh image-generation apps for artwork, product mockups, concept art, marketing visuals, illustrations, image editing, and upscaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask users to run mutable remote installers that can execute code on their machine.

Mitigation: Review the installer before use, prefer a pinned or manual install with independent checksum or signature verification, and avoid running setup from an elevated shell.

Risk: Prompts, images, image URLs, and account data may be disclosed to inference.sh and selected model providers.

Mitigation: Do not submit confidential prompts, images, URLs, or account data unless disclosure to those services and providers is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/ai-image-generation)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Image Generation Example](https://inference.sh/docs/examples/image-generation)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to produce inference.sh CLI commands and input JSON for selected image-generation apps.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
