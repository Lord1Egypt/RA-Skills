## Description: <br>
Image super-resolution tool: enhances image clarity and details, returning enhanced URL, suitable for low-res asset restoration and upscaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to upscale or restore low-resolution images from a URL or local image path through the dLazy CLI and hosted super-resolution service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be saved in local CLI configuration or provided through an environment variable. <br>
Mitigation: Use the documented dLazy login or key setup flow, keep the key scoped to the intended organization, and rotate or revoke it from the dLazy dashboard when access changes. <br>
Risk: Selected local image files or URLs are uploaded to dLazy hosted services for processing. <br>
Mitigation: Process only images the user intends to send to dLazy, and avoid sensitive or restricted content unless the user's policy permits that upload. <br>
Risk: The release installs or runs @dlazy/cli@latest, so the exact CLI package version is not pinned. <br>
Mitigation: Prefer npx for one-off use when a persistent install is unnecessary, and review the current @dlazy/cli package before installation. <br>


## Reference(s): <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [JSON result from the dLazy CLI with image output URLs, plus concise Markdown guidance for setup and error handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dLazy CLI, a dLazy API key, and network access to dLazy API and file endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
