## Description: <br>
Generate dynamic videos based on a single first frame image and prompts using Jimeng. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call the dLazy Jimeng image-to-video service from a shell workflow, supplying a prompt and first-frame image to generate a dynamic video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which may be stored in local CLI configuration or supplied through an environment variable. <br>
Mitigation: Use the dLazy login or auth flow intentionally, restrict local config access to the current OS user, and rotate or revoke the key from the dLazy dashboard if exposure is suspected. <br>
Risk: Prompts and selected local image files are sent to dLazy-hosted API and media storage endpoints for generation. <br>
Mitigation: Avoid using sensitive media or prompts unless upload to dLazy is acceptable for the user and organization. <br>


## Reference(s): <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-jimeng-i2v-first) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON responses and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is returned as hosted output URLs; asynchronous runs can return a generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
