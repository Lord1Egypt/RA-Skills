## Description: <br>
1MP raster image generation with refined design judgment for everyday creative work and fast iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to invoke dLazy's Recraft V4 image generation from an agent workflow and receive generated image results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and can store credentials in the local dLazy CLI configuration. <br>
Mitigation: Use the documented login or auth flow, keep the local config restricted to the current OS user, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts, parameters, and referenced local media files are sent to dLazy services for cloud inference and hosted output delivery. <br>
Mitigation: Send only content approved for dLazy processing, review the service terms before uploading sensitive files, and inspect requested network and credential use before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-recraft-v4) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON response containing generated image metadata and hosted result URLs, with Markdown guidance and shell commands for setup and invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be synchronous image results or asynchronous task identifiers that require polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
