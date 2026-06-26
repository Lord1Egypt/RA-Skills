## Description: <br>
Generates new images and transforms source images through Cloudflare Workers AI text-to-image and image-to-image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slippersheepig](https://clawhub.ai/user/slippersheepig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Cloudflare Workers AI image generation or image-to-image transformations, then return the generated PNG to the current chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and img2img source images are sent to Cloudflare Workers AI. <br>
Mitigation: Confirm the user is comfortable sending that content to Cloudflare and avoid sensitive prompts or images. <br>
Risk: Cloudflare API credentials are required for inference. <br>
Mitigation: Use a least-privilege API token and keep credentials out of checked-in compose files and chat logs. <br>
Risk: Generated image files can remain on disk when saved outside temporary paths. <br>
Mitigation: Prefer temporary output paths and delete generated files after delivery unless the user explicitly asks to keep them. <br>


## Reference(s): <br>
- [Docker Compose environment example](references/docker-compose-env-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PNG image files with stdout file paths and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CF_ACCOUNT_ID and CF_API_TOKEN; img2img sends source images to Cloudflare Workers AI.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
