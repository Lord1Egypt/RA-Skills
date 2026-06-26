## Description: <br>
Dlazy Gpt Image 2 lets agents generate images from text and edit or synthesize images from reference inputs through the dLazy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create or edit images with prompts, optional reference images, and output settings such as size, format, and quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and explicit image inputs are sent to dLazy's hosted service, and generated files are hosted by dLazy. <br>
Mitigation: Avoid sending sensitive prompts or images unless the user accepts the service handling and hosting model. <br>
Risk: The dLazy API key may be saved in the local CLI configuration. <br>
Mitigation: Use per-invocation credentials when appropriate, protect the local config file, and rotate or revoke the key from the dLazy dashboard if it may be exposed. <br>
Risk: The install command tracks @latest rather than a fixed CLI version. <br>
Mitigation: Prefer npx for one-off use or review the dLazy CLI source and resolved package version before persistent installation. <br>


## Reference(s): <br>
- [Dlazy Gpt Image 2 on ClawHub](https://clawhub.ai/dlazyai/dlazy-gpt-image-2) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with bash commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image results are returned as hosted file URLs; asynchronous runs may return a task identifier for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
