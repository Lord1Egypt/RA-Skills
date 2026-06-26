## Description: <br>
Midjourney style generation, supports aspect ratio, Bot type, and output position (grid/U1-U4). Suitable for artistic and strongly stylized creative generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate stylized images through the dLazy hosted Midjourney-style CLI, with controls for prompt, aspect ratio, bot type, and grid or upscaled output selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs or invokes @dlazy/cli@latest, so CLI behavior can change after this skill release. <br>
Mitigation: Review the @dlazy/cli package before installation and use a controlled or pinned CLI version where repeatability is required. <br>
Risk: Authentication uses a dLazy API key that may be stored in ~/.dlazy/config.json. <br>
Mitigation: Use DLAZY_API_KEY for temporary sessions when persistence is not desired, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and any media files explicitly passed to the CLI are sent to dLazy cloud endpoints for generation. <br>
Mitigation: Avoid submitting sensitive prompts or files unless approved for dLazy processing, and review dLazy service terms before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-mj-imagine) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with CLI commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; completed generations return image metadata and files.dlazy.com result URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
