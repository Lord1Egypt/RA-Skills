## Description: <br>
Generate/edit high-quality images with Nano Banana 2.0. Supports text-to-image and image-to-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to invoke the dLazy Banana2 CLI for text-to-image and image-to-image generation from prompts and optional image inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dLazy CLI can store an API key in local configuration. <br>
Mitigation: Prefer per-invocation DLAZY_API_KEY where appropriate, and rotate or revoke saved keys if local configuration is no longer trusted. <br>
Risk: Local files passed as image inputs may be uploaded to dLazy-hosted services. <br>
Mitigation: Avoid passing sensitive local files unless the user intends those files to be uploaded for image generation. <br>
Risk: Global installation persists a third-party CLI on the system. <br>
Mitigation: Prefer npx for on-demand use or review the @dlazy/cli source before installing globally. <br>


## Reference(s): <br>
- [Dlazy Banana2 ClawHub release](https://clawhub.ai/dlazyai/dlazy-banana2) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The invoked CLI returns JSON containing generated image output URLs or asynchronous task status.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
