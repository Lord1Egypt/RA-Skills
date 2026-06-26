## Description: <br>
Generate AI images with FLUX, Gemini, Grok, Seedream, Reve, and 50+ models via the inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to generate, edit, upscale, and combine images through inference.sh image models from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external CLI installer and service account for image generation. <br>
Mitigation: Install only after trusting inference.sh, prefer manual installation or checksum verification, and log in with the intended account. <br>
Risk: Prompts, image URLs, or source images may be sent to external image-generation providers through inference.sh. <br>
Mitigation: Do not submit confidential prompts, private images, secrets, internal URLs, or regulated data unless the provider handling and account impact are acceptable. <br>
Risk: Generation requests may consume account quota or incur billing impact. <br>
Mitigation: Confirm the active inference.sh account and quota or billing expectations before running commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/ai-image-generation) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Image Generation Example](https://inference.sh/docs/examples/image-generation) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompts, model selections, and infsh CLI commands; generated image assets are produced by the external inference.sh service.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
