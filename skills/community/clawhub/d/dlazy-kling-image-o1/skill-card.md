## Description: <br>
Generate exquisite images with the Kling o1 model, supporting text-to-image and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call the dLazy hosted Kling Image O1 service from an agent for image generation or image editing. It supports prompt-only generation, reference-image inputs, optional asynchronous execution, and JSON result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store or read credentials through the dLazy CLI. <br>
Mitigation: Use OS-user-restricted config or DLAZY_API_KEY per invocation, and rotate or revoke the key from the dLazy dashboard if needed. <br>
Risk: Prompts and selected local media files are sent to dLazy API and media storage endpoints for cloud generation. <br>
Mitigation: Avoid passing sensitive prompts or local files, and use dry-run behavior when available to inspect payload and cost before calling the API. <br>
Risk: Generation can fail because of missing credentials, insufficient credits, service errors, or asynchronous task failures. <br>
Mitigation: Handle unauthorized and insufficient-balance responses explicitly, and use the CLI's async polling or timeout options for long-running tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-kling-image-o1) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SKILL-cn.md](artifact/SKILL-cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns generated image URLs hosted on files.dlazy.com; async mode can return a task generateId for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
