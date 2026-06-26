## Description: <br>
Generates AI images with Nano Banana models, splits results into 2/4/6/9 grids, manages gallery downloads, and supports five UI languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local web interface for AI image generation, image-to-image editing, grid splitting, gallery management, and batch download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web server exposes unauthenticated file, credential, shutdown, and host-interaction capabilities. <br>
Mitigation: Install only for a trusted single-user local setup and do not expose port 2688 to a LAN or the internet. <br>
Risk: Prompts, uploaded images, and API keys may be sent to external providers during image generation, image upload, or prompt generation. <br>
Mitigation: Avoid sensitive API keys, private images, or confidential prompt content unless the configured providers and data handling are acceptable. <br>
Risk: Upload-by-path, open-folder, shutdown, and prompt/config editing endpoints can affect the host environment. <br>
Mitigation: Review or disable those endpoints before use in any shared or production environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiyunnet/banana-v2) <br>
- [Project homepage](https://banana2.zjhn.com) <br>
- [AceData API key setup](https://share.acedata.cloud/r/1uN88BrUTQ) <br>
- [Chinese documentation](docs/zh/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Files, Configuration instructions, Shell commands] <br>
**Output Format:** [Local web application output with generated image files, split image files, gallery metadata, and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied API credentials for image generation and optional prompt generation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
