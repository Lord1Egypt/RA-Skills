## Description: <br>
Generate diverse design-style images with Recraft v3, supporting text-to-image and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and external users use this skill to have an agent invoke dLazy's Recraft v3 CLI for image generation from prompts and optional input images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, parameters, and explicitly supplied local files may be sent to dLazy's hosted service. <br>
Mitigation: Avoid submitting sensitive prompts or files unless the user accepts dLazy processing; review inputs before invoking the CLI. <br>
Risk: Authentication may persist an API key in local CLI configuration. <br>
Mitigation: Use per-invocation DLAZY_API_KEY or npx when less local persistence is preferred, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Generated outputs are hosted by dLazy and API usage may consume account credits. <br>
Mitigation: Confirm cost-sensitive runs with dry-run or account checks when appropriate, and share hosted output URLs only with intended recipients. <br>


## Reference(s): <br>
- [Dlazy Recraft V3 on ClawHub](https://clawhub.ai/dlazyai/dlazy-recraft-v3) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image outputs are returned as dLazy-hosted URLs; asynchronous runs may return a task identifier for polling.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
