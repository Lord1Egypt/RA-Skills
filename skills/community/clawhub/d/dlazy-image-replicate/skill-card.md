## Description: <br>
Image replicate tool: analyzes the visuals, composition, colors, lighting, and style of the source image, builds a replicate prompt, and hands it off to Seedream 4.5 to generate a new image in the same style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external agents use this skill to analyze a reference image and request a new image in a similar visual style through the dLazy hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can store it in the local CLI configuration. <br>
Mitigation: Use the documented login or environment-variable flow, protect the local config file, and rotate or revoke the key from the dLazy dashboard when needed. <br>
Risk: Prompts, parameters, and referenced local media are sent to dLazy API and file storage endpoints for cloud inference. <br>
Mitigation: Review source images and prompts before invocation, avoid submitting sensitive media unless appropriate for the user's dLazy organization, and use dry-run behavior when checking payloads or cost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-image-replicate) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Images, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result payloads containing generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return synchronous image outputs or an asynchronous generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
