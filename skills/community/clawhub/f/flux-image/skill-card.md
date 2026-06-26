## Description: <br>
Generate images with FLUX models from Black Forest Labs through the inference.sh CLI, including text-to-image, image-to-image, and LoRA-based style adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and image-generation users use this skill to install and run inference.sh commands for FLUX image generation, image-to-image transformation, and LoRA-based style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install and run the inference.sh CLI from an external installer. <br>
Mitigation: Install only if inference.sh is trusted; review the installer or use the published checksum verification path before running it. <br>
Risk: Prompts, image URLs, LoRA inputs, or source images may be sent to external image-generation services. <br>
Mitigation: Avoid confidential prompts, private image URLs, secrets, or sensitive images unless that use is approved for the workflow. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Image Generation Example](https://inference.sh/docs/examples/image-generation) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/flux-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may invoke external inference.sh services that generate image outputs.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
