## Description: <br>
Text-to-image generation with Jimeng, quickly converting text to high-quality images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to invoke the dLazy Jimeng text-to-image CLI from an agent, sending prompts and optional reference images to generate image URLs through dLazy's hosted service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be stored locally or passed through the environment. <br>
Mitigation: Use a scoped dLazy organization key, keep the local CLI config protected, and rotate or revoke the key from the dLazy dashboard when needed. <br>
Risk: Prompts and referenced local images are sent to dLazy's hosted service for generation. <br>
Mitigation: Avoid passing private files or sensitive prompt content unless the user intends to upload them to the hosted service. <br>
Risk: The skill installs or runs the third-party @dlazy/cli package. <br>
Mitigation: Review the package or source before installation and prefer the pinned version declared by the skill metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-jimeng-t2i) <br>
- [dLazy CLI homepage](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Images, Guidance] <br>
**Output Format:** [JSON responses from the dLazy CLI with generated image URLs, plus concise command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; supports asynchronous generation with a generateId for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
