## Description: <br>
Generate and edit images with Nano Banana Pro, supporting text-to-image and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create or modify images through the dLazy Banana Pro CLI. It supports prompt-driven generation, reference-image editing, synchronous results, and asynchronous task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected local image files may be uploaded to dLazy-hosted endpoints for generation or editing. <br>
Mitigation: Avoid using the skill with private or sensitive prompts and images unless the user is comfortable sending that content to dLazy. <br>
Risk: The dLazy CLI may store an API key in the local user configuration. <br>
Mitigation: Use the npx invocation or the DLAZY_API_KEY environment variable for per-run credentials when avoiding a persistent global CLI or saved key is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-banana-pro) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON, images] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON result envelopes containing generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI may return image output URLs immediately or return an asynchronous generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
